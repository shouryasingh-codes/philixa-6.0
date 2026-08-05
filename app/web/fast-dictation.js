// Web Speech API Implementation for Fast Dictation
// Completely isolated from the Whisper/Live Recording logic

document.addEventListener("DOMContentLoaded", () => {
  const tabFastDictationBtn = document.getElementById("tabFastDictationBtn");
  const viewFastDictation = document.getElementById("viewFastDictation");
  
  const startDictationBtn = document.getElementById("startDictationBtn");
  const stopDictationBtn = document.getElementById("stopDictationBtn");
  const dictationStatusText = document.getElementById("dictationStatusText");
  const dictationResult = document.getElementById("dictationResult");
  
  // Elements from existing app to switch tabs and dump text
  const viewText = document.getElementById("viewText");
  const viewAudio = document.getElementById("viewAudio");
  const viewLive = document.getElementById("viewLive");
  const tabTextBtn = document.getElementById("tabTextBtn");
  const tabAudioBtn = document.getElementById("tabAudioBtn");
  const tabLiveBtn = document.getElementById("tabLiveBtn");
  
  const rawNotes = document.getElementById("rawNotes");

  let recognition = null;
  let finalTranscript = "";

  // Check if browser supports Web Speech API
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  
  if (!SpeechRecognition) {
    dictationStatusText.textContent = "❌ Not supported in this browser (Use Chrome)";
    startDictationBtn.disabled = true;
  } else {
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    // Set to en-IN. This works perfectly on Chrome for Hinglish
    // Chrome translates spoken Hindi into English alphabet automatically with en-IN
    recognition.lang = 'en-IN'; 

    recognition.onstart = () => {
      dictationStatusText.textContent = "🔴 Recording... Speak now";
      startDictationBtn.disabled = true;
      stopDictationBtn.disabled = false;
      finalTranscript = "";
      dictationResult.innerHTML = "";
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error", event.error);
      dictationStatusText.textContent = `❌ Error: ${event.error}`;
      startDictationBtn.disabled = false;
      stopDictationBtn.disabled = true;
    };

    recognition.onend = () => {
      // If stopped naturally or by button
      dictationStatusText.textContent = "⏸ Ready (Web Speech API)";
      startDictationBtn.disabled = false;
      stopDictationBtn.disabled = true;
    };

    recognition.onresult = (event) => {
      let interimTranscript = "";
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript + " ";
        } else {
          interimTranscript += event.results[i][0].transcript;
        }
      }
      
      dictationResult.innerHTML = `
        <span style="font-weight:600; color:var(--text);">${finalTranscript}</span>
        <span style="color:var(--muted); font-style:italic;">${interimTranscript}</span>
      `;
    };
  }

  // --- UI Interactions ---

  tabFastDictationBtn.addEventListener("click", () => {
    // Make this tab active
    tabFastDictationBtn.classList.add("active");
    viewFastDictation.classList.remove("hidden");
    viewFastDictation.style.display = "block";
    
    // Deactivate others
    [tabTextBtn, tabAudioBtn, tabLiveBtn].forEach(btn => {
      if(btn) btn.classList.remove("active");
    });
    
    [viewText, viewAudio, viewLive].forEach(view => {
      if(view) {
        view.classList.add("hidden");
        view.classList.remove("active");
        view.style.display = "none";
      }
    });
  });

  // Make sure clicking other tabs hides Fast Dictation
  [tabTextBtn, tabAudioBtn, tabLiveBtn].forEach(btn => {
    if(!btn) return;
    btn.addEventListener("click", () => {
      tabFastDictationBtn.classList.remove("active");
      viewFastDictation.classList.add("hidden");
      viewFastDictation.style.display = "none";
      // Stop recognition if active
      if (recognition && !startDictationBtn.disabled) {
          // It's not running
      } else if (recognition) {
          recognition.stop();
      }
    });
  });

  startDictationBtn.addEventListener("click", () => {
    if (recognition) {
      try {
        recognition.start();
      } catch (e) {
        console.error(e);
      }
    }
  });

  stopDictationBtn.addEventListener("click", () => {
    if (recognition) {
      recognition.stop();
      
      // Auto-switch to Text tab and paste notes
      if (finalTranscript.trim()) {
        const textToPaste = finalTranscript.trim();
        rawNotes.value = textToPaste;
        
        // Emulate clicking the Text tab
        tabTextBtn.click();
      }
    }
  });
});
