// Philixa Voice Assistant - Continuous Loop Logic

let voiceState = "idle";
let voiceWs = null;
let voiceAudioContext = null;
let voiceWorkletNode = null;
let voiceAudioStream = null;
let conversationHistory = [];
let silenceTimeout = null;
const SILENCE_LIMIT_MS = 3000;

function initVoice() {
    const fabBtn = document.getElementById("philixaVoiceBtn");
    if (fabBtn) {
        fabBtn.addEventListener("click", handleVoiceClick);
    }
}
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initVoice);
} else {
    initVoice();
}

function setVoiceState(state) {
    voiceState = state;
    const fabBtn = document.getElementById('philixaVoiceBtn');
    if (!fabBtn) return;
    
    const icon = fabBtn.querySelector('.copilot-icon');
    const text = fabBtn.querySelector('.copilot-text');
    
    fabBtn.className = 'copilot-box';
    fabBtn.style.background = ''; 
    
    if (state === 'idle') {
        if(icon) icon.textContent = '🎙️';
        if(text) text.textContent = 'PHILIXA';
    } else if (state === 'listening') {
        fabBtn.classList.add('listening');
        if(icon) icon.textContent = '🔴';
        if(text) text.textContent = 'LISTENING...';
    } else if (state === 'thinking') {
        fabBtn.classList.add('thinking');
        if(icon) icon.textContent = '🤔';
        if(text) text.textContent = 'THINKING...';
    } else if (state === 'speaking') {
        fabBtn.classList.add('speaking');
        if(icon) icon.textContent = '💬';
        if(text) text.textContent = 'SPEAKING...';
    }
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

        voiceAudioContext = new window.AudioContext({ sampleRate: 48000 });
        try {
            await voiceAudioContext.audioWorklet.addModule("/static/pcm-processor.js");
        } catch (err) {
            console.error("AudioWorklet load failed:", err);
            setVoiceState("idle");
            return;
        }

        const source = voiceAudioContext.createMediaStreamSource(voiceAudioStream);
        voiceWorkletNode = new AudioWorkletNode(voiceAudioContext, "pcm-processor");

        const apiKeyEl = document.getElementById("apiKey");
        const apiKey = apiKeyEl ? apiKeyEl.value : "";
        
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = protocol + "//" + window.location.host + "/api/v1/live/transcribe?api_key=" + apiKey + "&sample_rate=48000&diarize=false";
        
        voiceWs = new WebSocket(wsUrl);
        voiceWs.binaryType = "arraybuffer";

        voiceWs.onopen = () => {
            console.log("[Philixa Voice] Connected to Deepgram.");
            resetSilenceTimer();
        };

        voiceWs.onmessage = async (event) => {
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
            if (voiceWs && voiceWs.readyState === WebSocket.OPEN) {
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
    setVoiceState("thinking");
    
    if (voiceWorkletNode) voiceWorkletNode.disconnect();
    if (voiceAudioContext) voiceAudioContext.close();
    if (voiceAudioStream) voiceAudioStream.getTracks().forEach((t) => t.stop());

    if (voiceWs && voiceWs.readyState === WebSocket.OPEN) {
        voiceWs.send(JSON.stringify({ action: "stop" }));
    }
}

async function processUserTranscript(transcript) {
    if (!transcript || transcript.trim() === "") {
        console.log("[Philixa Voice] Empty transcript ignored.");
        setVoiceState("idle");
        return;
    }
    
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

function resetSilenceTimer() {
    if (silenceTimeout) clearTimeout(silenceTimeout);
    silenceTimeout = setTimeout(() => {
        console.log("[Philixa Voice] Silence detected. Stopping recording.");
        if (voiceState === "listening") {
            stopVoiceListening();
        }
    }, SILENCE_LIMIT_MS);
}
