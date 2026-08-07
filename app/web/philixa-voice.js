// Philixa Voice Assistant - Continuous Loop Logic

let voiceState = "idle"; // idle, listening, thinking, speaking
let voiceWs = null;
let voiceAudioContext = null;
let voiceWorkletNode = null;
let voiceAudioStream = null;
let conversationHistory = [];
let silenceTimeout = null;
const SILENCE_LIMIT_MS = 2500; // 2.5 seconds of silence turns it off automatically

document.addEventListener("DOMContentLoaded", () => {
    const fabBtn = document.getElementById("philixaVoiceBtn");
    if (fabBtn) {
        fabBtn.addEventListener("click", handleVoiceClick);
    }
});

function setVoiceState(state) {
    voiceState = state;
    const fabBtn = document.getElementById("philixaVoiceBtn");
    const icon = fabBtn.querySelector(".fab-icon");
    
    // Reset all classes and inline styles
    fabBtn.className = "fab-voice-btn";
    fabBtn.style.background = ""; // Clear inline background overrides
    
    if (state === "idle") {
        icon.textContent = "🎙️";
    } else if (state === "listening") {
        fabBtn.classList.add("listening");
        icon.textContent = "👂";
    } else if (state === "thinking") {
        fabBtn.style.background = "linear-gradient(135deg, #3b82f6, #2563eb)"; // Blue for thinking
        icon.textContent = "🧠";
    } else if (state === "speaking") {
        fabBtn.style.background = "linear-gradient(135deg, #eab308, #ca8a04)"; // Yellow for speaking
        icon.textContent = "🔊";
    }
}

function resetSilenceTimer() {
    if (silenceTimeout) clearTimeout(silenceTimeout);
    silenceTimeout = setTimeout(() => {
        if (voiceState === "listening") {
            console.log("[Philixa Voice] Auto-off triggered due to silence.");
            stopVoiceListening();
        }
    }, SILENCE_LIMIT_MS);
}

async function handleVoiceClick() {
    if (voiceState === "idle") {
        await startVoiceListening();
    } else if (voiceState === "listening") {
        await stopVoiceListening();
    }
}

async function startVoiceListening() {
    try {
        setVoiceState("listening");
        
        voiceAudioStream = await navigator.mediaDevices.getUserMedia({
            audio: { channelCount: 1, sampleRate: 48000, echoCancellation: true, noiseSuppression: true }
        });

        voiceAudioContext = new AudioContext({ sampleRate: 48000 });
        try {
            await voiceAudioContext.audioWorklet.addModule("/static/pcm-processor.js");
        } catch (err) {
            console.error("AudioWorklet load failed:", err);
            setVoiceState("idle");
            return;
        }

        const source = voiceAudioContext.createMediaStreamSource(voiceAudioStream);
        voiceWorkletNode = new AudioWorkletNode(voiceAudioContext, "pcm-processor");

        // Use the existing api key logic from the page if available
        const apiKeyEl = document.getElementById("apiKey");
        const apiKey = apiKeyEl ? apiKeyEl.value : "";
        
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        // We use the same STT endpoint that was just fixed for Hindi/Hinglish
        const wsUrl = `${protocol}//${window.location.host}/api/v1/live/transcribe?api_key=${apiKey}&sample_rate=48000&diarize=false`;
        
        voiceWs = new WebSocket(wsUrl);
        voiceWs.binaryType = "arraybuffer";

        voiceWs.onopen = () => {
            console.log("[Philixa Voice] Connected to Deepgram.");
            resetSilenceTimer(); // Start the silence timer when connected
        };

        voiceWs.onmessage = async (event) => {
            // Any message (even interim or empty) resets the silence timer as long as user is making noise
            resetSilenceTimer();
            
            const data = JSON.parse(event.data);
            if (data.action === "stopped" && data.confirmed) {
                const transcript = data.confirmed.trim();
                console.log("[Philixa Voice] Heard:", transcript);
                await processUserTranscript(transcript);
            } else if (data.action === "stopped" && !data.confirmed) {
                setVoiceState("idle");
            }
        };

        voiceWorkletNode.port.onmessage = (event) => {
            if (voiceWs?.readyState === WebSocket.OPEN) {
                voiceWs.send(event.data);
            }
        };

        source.connect(voiceWorkletNode);
        voiceWorkletNode.connect(voiceAudioContext.destination);
    } catch (err) {
        console.error("Voice listening failed:", err);
        setVoiceState("idle");
    }
}

async function stopVoiceListening() {
    if (silenceTimeout) clearTimeout(silenceTimeout);
    setVoiceState("thinking"); // Transition to thinking while waiting for transcript
    
    if (voiceWorkletNode) voiceWorkletNode.disconnect();
    if (voiceAudioContext) voiceAudioContext.close();
    if (voiceAudioStream) voiceAudioStream.getTracks().forEach((t) => t.stop());

    if (voiceWs?.readyState === WebSocket.OPEN) {
        voiceWs.send(JSON.stringify({ action: "stop" }));
    }
}

async function processUserTranscript(transcript) {
    try {
        setVoiceState("thinking");
        
        const response = await fetch("/api/v1/voice/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text: transcript,
                conversation_history: conversationHistory
            })
        });

        if (!response.ok) throw new Error("Chat API failed");
        
        const data = await response.json();
        const aiResponseText = data.response;
        
        console.log("[Philixa Voice] AI Response:", aiResponseText);
        
        // Save to history
        conversationHistory.push({ role: "user", content: transcript });
        conversationHistory.push({ role: "assistant", content: aiResponseText });
        
        await speakAIResponse(aiResponseText);
    } catch (err) {
        console.error("[Philixa Voice] Process error:", err);
        setVoiceState("idle");
    }
}

async function speakAIResponse(text) {
    try {
        setVoiceState("speaking");
        
        const response = await fetch("/api/v1/voice/speak", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) throw new Error("TTS API failed");

        const blob = await response.blob();
        const audioUrl = URL.createObjectURL(blob);
        const audio = new Audio(audioUrl);
        
        audio.onended = () => {
            // Check if the AI ended with a question (like "Should I save this?")
            // If yes, we automatically go back to listening!
            if (text.includes("?") || text.toLowerCase().includes("save")) {
                startVoiceListening();
            } else {
                setVoiceState("idle");
            }
        };
        
        await audio.play();
    } catch (err) {
        console.error("[Philixa Voice] TTS error:", err);
        setVoiceState("idle");
    }
}
