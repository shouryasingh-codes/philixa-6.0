const state = {
  clients: [],
  commitments: [],
  priorities: { tasks: [], risks: [] },
  selectedClientId: null,
  pendingConfirmationMeetingId: null,
};

const els = {
  editTranscriptPanel: document.querySelector("#editTranscriptPanel"),
  editTranscriptText: document.querySelector("#editTranscriptText"),
  saveTranscriptBtn: document.querySelector("#saveTranscriptBtn"),
  apiKey: document.querySelector("#apiKey"),
  toggleKey: document.querySelector("#toggleKey"),
  healthDot: document.querySelector("#healthDot"),
  healthText: document.querySelector("#healthText"),
  clientCount: document.querySelector("#clientCount"),
  pendingCount: document.querySelector("#pendingCount"),
  topClientSelect: document.querySelector("#topClientSelect"),
  rawNotes: document.querySelector("#rawNotes"),
  meetingDate: document.querySelector("#meetingDate"),
  knownClient: document.querySelector("#knownClient"),
  processNotes: document.querySelector("#processNotes"),
  processResult: document.querySelector("#processResult"),
  confirmPanel: document.querySelector("#confirmPanel"),
  confirmClientSelect: document.querySelector("#confirmClientSelect"),
  newClientName: document.querySelector("#newClientName"),
  confirmClient: document.querySelector("#confirmClient"),
  loadSelectedMemory: document.querySelector("#loadSelectedMemory"),
  memoryContent: document.querySelector("#memoryContent"),
  commitmentFilter: document.querySelector("#commitmentFilter"),
  commitmentRows: document.querySelector("#commitmentRows"),
  taskList: document.querySelector("#taskList"),
  riskList: document.querySelector("#riskList"),
  toast: document.querySelector("#toast"),
  askClientSection: document.querySelector("#askClientSection"),
  askClientInput: document.querySelector("#askClientInput"),
  askClientBtn: document.querySelector("#askClientBtn"),
  askClientResult: document.querySelector("#askClientResult"),
  themeToggleBtn: document.querySelector("#themeToggleBtn"),
  settingsBtn: document.querySelector("#settingsBtn"),
  settingsModal: document.querySelector("#settingsModal"),
  closeSettingsBtn: document.querySelector("#closeSettingsBtn"),
  prefOptIn: document.querySelector("#prefOptIn"),
  prefContact: document.querySelector("#prefContact"),
  prefQuietStart: document.querySelector("#prefQuietStart"),
  prefQuietEnd: document.querySelector("#prefQuietEnd"),
  saveSettingsBtn: document.querySelector("#saveSettingsBtn"),
  tabTextBtn: document.querySelector("#tabTextBtn"),
  tabAudioBtn: document.querySelector("#tabAudioBtn"),
  viewText: document.querySelector("#viewText"),
  viewAudio: document.querySelector("#viewAudio"),
  audioFileInput: document.querySelector("#audioFileInput"),
  uploadFileName: document.querySelector("#uploadFileName"),
  processAudio: document.querySelector("#processAudio"),
  meetingDateAudio: document.querySelector("#meetingDateAudio"),
  audioStatusBox: document.querySelector("#audioStatusBox"),
  audioStatusText: document.querySelector("#audioStatusText"),
  audioStatusDetails: document.querySelector("#audioStatusDetails"),
  uploadBox: document.querySelector("#uploadBox"),
  meetingDateAudio: document.querySelector("#meetingDateAudio"),
};

let currentAudio = null;

async function playTTS(text) {
  try {
    if (currentAudio) {
      currentAudio.pause();
      currentAudio = null;
    }
    const res = await fetch('/api/v1/voice/speak', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey()
      },
      body: JSON.stringify({ text })
    });
    if (!res.ok) {
      console.log('TTS not enabled or failed', res.status);
      return;
    }
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    currentAudio = new Audio(url);
    currentAudio.play();
  } catch (err) {
    console.error('TTS Error:', err);
  }
}

function todayIso() {
  return new Date().toISOString().slice(0, 10);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatShortDate(dateString) {
  if (!dateString || typeof dateString !== "string") return dateString || "Unknown";
  const match = dateString.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!match) return dateString;
  const d = new Date(match[1], match[2] - 1, match[3]);
  if (isNaN(d)) return dateString;
  return d.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
}

function showToast(message, isError = false) {
  els.toast.textContent = message;
  els.toast.classList.toggle("error", isError);
  els.toast.classList.add("show");
  window.setTimeout(() => els.toast.classList.remove("show"), 2600);
}

function apiKey() {
  return els.apiKey.value.trim() || "philixa-demo-secret-123";
}

async function api(path, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    "X-API-Key": apiKey(),
    ...(options.headers || {}),
  };
  const response = await fetch(path, { ...options, headers });
  if (!response.ok) {
    let detail = `Request failed with ${response.status}`;
    try {
      const payload = await response.json();
      detail = payload.detail || detail;
    } catch {
      detail = response.statusText || detail;
    }
    throw new Error(detail);
  }
  return response.json();
}

async function checkHealth() {
  try {
    const payload = await fetch("/health").then((res) => res.json());
    els.healthDot.className = "status-dot ok";
    els.healthText.textContent = `API ${payload.status} - DB ${payload.database}`;
  } catch {
    els.healthDot.className = "status-dot error";
    els.healthText.textContent = "API offline";
  }
}

function clientNameById(clientId) {
  const match = state.clients.find((client) => client.id === Number(clientId));
  return match ? match.name : `Client #${clientId}`;
}

function updateMetrics() {
  els.clientCount.textContent = state.clients.length;
  els.pendingCount.textContent = state.commitments.filter((item) => item.status === "pending").length;
  els.topClientSelect.value = state.selectedClientId || "";
}

function renderClientOptions() {
  const clientOptions = state.clients
    .map((client) => `<option value="${client.id}">${escapeHtml(client.name)}</option>`)
    .join("");
  els.knownClient.innerHTML = `<option value="">Auto identify client</option>${clientOptions}`;
  els.confirmClientSelect.innerHTML = `<option value="">Select existing client</option>${clientOptions}`;
  els.topClientSelect.innerHTML = `<option value="">No client selected</option>${clientOptions}`;
  els.topClientSelect.value = state.selectedClientId || "";
}

function renderClients() {
  renderClientOptions();
  updateMetrics();
}

function renderCommitments() {
  if (!state.commitments.length) {
    els.commitmentRows.innerHTML = `<tr><td colspan="6" class="muted">No commitments found.</td></tr>`;
    updateMetrics();
    return;
  }
  els.commitmentRows.innerHTML = state.commitments
    .map((item) => {
      const nextStatus = item.status === "pending" ? "completed" : "pending";
      const label = item.status === "pending" ? "Complete" : "Reopen";
      const pillClass = item.status === "completed" ? "done" : "";
      return `
        <tr>
          <td>${escapeHtml(clientNameById(item.client_id))}</td>
          <td>
            <div class="commitment-title">${escapeHtml(item.description)}</div>
            <div class="client-meta">Owner: ${escapeHtml(item.owner)} - Confidence: ${Math.round((item.extraction_confidence || 0) * 100)}%</div>
          </td>
          <td>${escapeHtml(formatShortDate(item.due_date || item.due_date_text))}</td>
          <td><span class="status-pill urgency-${escapeHtml(item.urgency_level || "medium")}">${escapeHtml(item.urgency_level || "medium")}</span></td>
          <td><span class="status-pill ${pillClass}">${escapeHtml(item.status)}</span></td>
          <td><button class="link-button" type="button" data-commitment-id="${item.id}" data-next-status="${nextStatus}">${label}</button></td>
        </tr>
      `;
    })
    .join("");
  updateMetrics();
}

function renderProcessResult(payload) {
  const statusClass = payload.requires_client_confirmation ? "warning" : "done";
  const created = payload.commitments_created || [];
  const updated = payload.commitments_updated || [];
  const pending = payload.pending_commitments || [];
  els.processResult.innerHTML = `
    <div class="result-summary">
      <span class="status-pill ${statusClass}">${escapeHtml(payload.client_status)}</span>
      <strong>${escapeHtml(payload.meeting_summary || "Meeting processed.")}</strong>
      <span class="muted">Created: ${created.length} - Updated: ${updated.length} - Pending: ${pending.length}</span>
      ${pending.length ? `<ul>${pending.map((item) => `<li>${escapeHtml(item.description)} - ${escapeHtml(item.due_date || item.due_date_text || "Unknown due date")}</li>`).join("")}</ul>` : ""}
      ${payload.warnings && payload.warnings.length ? `<span class="muted">${payload.warnings.map(escapeHtml).join(" | ")}</span>` : ""}
    </div>
  `;
  if (payload.requires_client_confirmation) {
    state.pendingConfirmationMeetingId = payload.meeting_id;
    els.confirmPanel.classList.remove("hidden");
    
    // Auto-fill suggested client name if extracted by AI
    const suggestedName = payload.extraction?.client_identification?.suggested_client_name || "";
    els.newClientName.value = suggestedName;
  } else {
    state.pendingConfirmationMeetingId = null;
    els.confirmPanel.classList.add("hidden");
    state.selectedClientId = payload.client_id;
  }
}

function renderMemory(payload) {
  const commitments = payload.pending_commitments || [];
  const concerns = payload.major_concerns || [];
  const notes = payload.recent_relationship_notes || [];
  const brief = payload.pre_meeting_brief || {};
  els.memoryContent.innerHTML = `
    <div class="brief-card">
      <div class="brief-card-header">
        <div>
          <span class="eyebrow">AI briefing</span>
          <h4>${escapeHtml(brief.title || "Client Brief")}</h4>
        </div>
        <span class="status-pill done">${escapeHtml(payload.client_name)}</span>
      </div>
      <div class="brief-grid">
        <div class="brief-block">
          <span class="brief-label">Last Meeting</span>
          <strong>${escapeHtml(brief.last_meeting || "No recent meeting")}</strong>
        </div>
        <div class="brief-block">
          <span class="brief-label">Pending</span>
          ${
            brief.pending && brief.pending.length
              ? `<ul>${brief.pending.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`
              : `<span class="muted">No pending commitment.</span>`
          }
        </div>
        <div class="brief-block">
          <span class="brief-label">Products</span>
          ${
            payload.products_owned && payload.products_owned.length
              ? `<strong>${payload.products_owned.map(escapeHtml).join(", ")}</strong>`
              : `<span class="muted">None recorded.</span>`
          }
        </div>
        <div class="brief-block">
          <span class="brief-label">Concern</span>
          <strong>${escapeHtml(brief.concern || "No major concern captured")}</strong>
        </div>
        <div class="brief-block">
          <span class="brief-label">Suggested Talking Point</span>
          <p>${escapeHtml(brief.suggested_talking_point || "Start with a quick recap and next step.")}</p>
        </div>
      </div>
    </div>
    <div class="memory-block narrative-block">
      <h4>AI Memory Narrative</h4>
      <p>${escapeHtml(payload.rolling_summary || payload.last_meeting_summary || "No rolling summary yet.")}</p>
    </div>
    <div class="memory-block">
      <h4>Last meeting summary</h4>
      <p>${escapeHtml(payload.last_meeting_summary || "No recent summary.")}</p>
    </div>
    <div class="memory-block">
      <h4>Pending commitments</h4>
      ${commitments.length ? `<ul>${commitments.map((item) => `<li>${escapeHtml(item.description)} - ${escapeHtml(formatShortDate(item.due_date || item.due_date_text))}</li>`).join("")}</ul>` : `<span class="muted">No pending commitments.</span>`}
    </div>
    <div class="memory-block">
      <h4>Concerns</h4>
      ${concerns.length ? `<ul>${concerns.map((item) => `<li>${escapeHtml(item.description || item)}</li>`).join("")}</ul>` : `<span class="muted">No concerns captured.</span>`}
    </div>
    <div class="memory-block">
      <h4>Recent notes</h4>
      ${notes.length ? `<ul>${notes.map((note) => `<li>${escapeHtml(note)}</li>`).join("")}</ul>` : `<span class="muted">No recent notes.</span>`}
    </div>
  `;
}

async function loadPriorities() {
  const payload = await api("/api/v1/dashboard/priorities");
  state.priorities.tasks = payload.tasks || [];
  state.priorities.risks = payload.risks || [];
  renderTasks();
  renderRisks();
}

function renderTasks() {
  const tasks = state.priorities.tasks;
  if (!tasks.length) {
    els.taskList.innerHTML = `<div class="empty-state">✅ All caught up! No pressing tasks for today.</div>`;
    return;
  }
  const today = todayIso();
  els.taskList.innerHTML = tasks
    .map((task) => {
      const due = task.due_date || "";
      let variant = "upcoming";
      let badgeLabel = due ? `Due ${due}` : "No due date";
      if (task.is_overdue || (due && due < today)) {
        variant = "overdue";
        badgeLabel = `Overdue — ${due}`;
      } else if (task.is_due_today || due === today) {
        variant = "due-today";
        badgeLabel = "Due today";
      }
      return `
        <div class="task-card ${variant}">
          <div class="task-card-title">${escapeHtml(task.description)}</div>
          <div class="task-card-meta">
            <span class="task-badge ${variant}">${escapeHtml(badgeLabel)}</span>
            <span class="client-meta">${escapeHtml(task.client_name || `Client #${task.client_id}`)}</span>
          </div>
        </div>
      `;
    })
    .join("");
}

function renderRisks() {
  const risks = state.priorities.risks;
  if (!risks.length) {
    els.riskList.innerHTML = `<div class="empty-state">🛡️ All clear. No active risk signals detected.</div>`;
    return;
  }
  els.riskList.innerHTML = risks
    .map((risk) => {
      const severity = (risk.severity_level || "medium").toLowerCase();
      const confidence = Math.round((risk.confidence || 0) * 100);
      return `
        <div class="risk-card ${severity}">
          <div class="risk-card-title">${escapeHtml(risk.description)}</div>
          <div class="risk-card-meta">
            <span class="risk-badge ${severity}">${escapeHtml(severity)}</span>
            <span class="task-badge ${risk.requires_review ? "overdue" : "upcoming"}">${risk.requires_review ? "Review needed" : "Monitoring"}</span>
            <span class="client-meta">${escapeHtml(risk.client_name || `Client #${risk.client_id}`)} &mdash; ${confidence}% confidence</span>
          </div>
        </div>
      `;
    })
    .join("");
}

async function loadClients() {
  state.clients = await api("/api/v1/clients");
  if (!state.selectedClientId && state.clients.length) {
    state.selectedClientId = state.clients[0].id;
  }
  renderClients();
}

async function loadCommitments() {
  const filter = els.commitmentFilter.value;
  const query = filter ? `?status=${encodeURIComponent(filter)}` : "";
  const payload = await api(`/api/v1/commitments${query}`);
  state.commitments = payload.commitments || [];
  renderCommitments();
}

async function loadMemory(clientId = state.selectedClientId) {
  if (!clientId) {
    showToast("Select a client first.", true);
    return;
  }
  const payload = await api(`/api/v1/clients/${clientId}/memory`);
  state.selectedClientId = Number(clientId);
  state.clients = state.clients.map((client) =>
    client.id === state.selectedClientId
      ? {
          ...client,
          rolling_summary: payload.rolling_summary,
          last_meeting_summary: payload.last_meeting_summary,
        }
      : client
  );
  renderMemory(payload);
  els.askClientSection.classList.remove("hidden");
  els.askClientInput.value = "";
  els.askClientResult.innerHTML = "";
  els.askClientResult.classList.add("hidden");
  renderClients();
}

async function askClient() {
  if (!state.selectedClientId) return;
  const query = els.askClientInput.value.trim();
  if (!query) return;

  els.askClientResult.classList.remove("hidden");
  els.askClientResult.innerHTML = `<span class="muted">Asking AI...</span>`;

  try {
    const payload = await api(`/api/v1/clients/${state.selectedClientId}/ask`, {
      method: "POST",
      body: JSON.stringify({ query }),
    });
    
    let answerHtml = `<p>${escapeHtml(payload.answer)}</p>`;
    if (payload.source_meetings && payload.source_meetings.length > 0) {
      answerHtml += `<p class="muted" style="margin-top: 0.5rem; font-size: 0.8rem;">Sources: Meetings ${payload.source_meetings.join(", ")}</p>`;
    }
    els.askClientResult.innerHTML = answerHtml;
  } catch (err) {
    els.askClientResult.innerHTML = `<span class="error" style="color: var(--danger)">${escapeHtml(err.message)}</span>`;
  }
}

async function refreshAll() {
  await checkHealth();
  await loadClients();
  await loadCommitments();
  await loadPriorities();
}

async function withLoading(button, label, fn) {
  if (button.disabled) return;
  const original = button.textContent;
  button.disabled = true;
  button.textContent = label;
  try {
    await fn();
  } finally {
    button.disabled = false;
    button.textContent = original;
  }
}

async function processNotes() {
  els.editTranscriptPanel.classList.add("hidden");
  const rawNotes = els.rawNotes.value.trim();
  if (!rawNotes) {
    showToast("Paste meeting notes first.", true);
    return;
  }
  const body = {
    raw_notes: rawNotes,
    meeting_date: els.meetingDate.value || undefined,
    known_client_id: els.knownClient.value ? Number(els.knownClient.value) : undefined,
  };
  const payload = await api("/api/v1/meeting-notes/process", {
    method: "POST",
    body: JSON.stringify(body),
  });
  renderProcessResult(payload);
  await refreshAll();
  if (payload.client_id) {
    await loadMemory(payload.client_id);
  }
  showToast("Meeting notes processed.");
}

async function confirmClient() {
  if (!state.pendingConfirmationMeetingId) {
    showToast("No meeting needs confirmation.", true);
    return;
  }
  const existingClientId = els.confirmClientSelect.value;
  const newClientName = els.newClientName.value.trim();
  if (!existingClientId && !newClientName) {
    showToast("Select a client or enter a new name.", true);
    return;
  }
  const payload = await api(`/api/v1/meeting-notes/${state.pendingConfirmationMeetingId}/confirm-client`, {
    method: "POST",
    body: JSON.stringify({
      client_id: existingClientId ? Number(existingClientId) : undefined,
      new_client_name: newClientName || undefined,
    }),
  });
  els.newClientName.value = "";
  els.confirmPanel.classList.add("hidden");
  renderProcessResult(payload);
  await refreshAll();
  if (payload.client_id) {
    await loadMemory(payload.client_id);
  }
  showToast("Client confirmed.");
}

async function updateCommitmentStatus(commitmentId, status) {
  await api(`/api/v1/commitments/${commitmentId}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });
  await loadCommitments();
  if (state.selectedClientId) {
    await loadMemory(state.selectedClientId);
  }
  showToast(`Commitment marked ${status}.`);
}

async function deleteClient(clientId) {
  const client = state.clients.find((item) => item.id === Number(clientId));
  const clientName = client ? client.name : `Client #${clientId}`;
  const confirmed = window.confirm(
    `Delete ${clientName}? This will permanently remove this client, meetings, and commitments.`
  );
  if (!confirmed) {
    return;
  }
  await api(`/api/v1/clients/${clientId}`, { method: "DELETE" });
  if (state.selectedClientId === Number(clientId)) {
    state.selectedClientId = null;
    els.memoryContent.innerHTML = `<span class="muted">Select a client to view instant context.</span>`;
    els.askClientSection.classList.add("hidden");
  }
  await refreshAll();
  if (state.selectedClientId) {
    await loadMemory(state.selectedClientId);
  }
  showToast(`${clientName} deleted.`);
}

async function openSettings() {
  els.settingsModal.classList.remove("hidden");
  try {
    const payload = await api("/api/v1/preferences");
    els.prefOptIn.checked = payload.is_opted_in;
    els.prefContact.value = payload.whatsapp_number || "";
    els.prefQuietStart.value = payload.quiet_hours_start || "";
    els.prefQuietEnd.value = payload.quiet_hours_end || "";
  } catch (err) {
    showToast(err.message, true);
  }
}

function closeSettings() {
  els.settingsModal.classList.add("hidden");
}

async function saveSettings() {
  const body = {
    is_opted_in: els.prefOptIn.checked,
    whatsapp_number: els.prefContact.value.trim() || null,
    quiet_hours_start: els.prefQuietStart.value || null,
    quiet_hours_end: els.prefQuietEnd.value || null,
  };
  try {
    await api("/api/v1/preferences", {
      method: "PUT",
      body: JSON.stringify(body),
    });
    showToast("Preferences saved.");
    closeSettings();
  } catch (err) {
    showToast(err.message, true);
  }
}


async function saveTranscript() {
  const meetingId = els.editTranscriptPanel.dataset.meetingId;
  const rawNotes = els.editTranscriptText.value.trim();
  
  if (!meetingId) {
    showToast("Meeting ID missing.", true);
    return;
  }
  if (!rawNotes) {
    showToast("Transcript cannot be empty.", true);
    return;
  }

  els.editTranscriptPanel.classList.add("hidden");
  els.processResult.innerHTML = `
    <div style="display: flex; align-items: center; gap: 10px; padding: 10px;">
      <span class="status-dot pulsing" style="background: var(--blue);"></span>
      <strong style="color: var(--blue);">Reprocessing transcript via AI... This may take a few seconds.</strong>
    </div>
  `;

  await api(`/api/v1/meeting-notes/${meetingId}/transcript`, {
    method: "PATCH",
    body: JSON.stringify({ raw_notes: rawNotes })
  });

  // Poll for background job completion
  const pollInterval = setInterval(async () => {
    try {
      const response = await fetch(`/api/v1/meeting-notes/${meetingId}`, {
        headers: { "X-API-Key": apiKey() }
      });
      if (response.ok) {
        const meeting = await response.json();
        if (meeting.status === 'processed') {
          clearInterval(pollInterval);
          
          renderProcessResult({
            meeting_id: meeting.id,
            client_status: meeting.client_identification_status || "identified",
            client_id: meeting.client_id,
            requires_client_confirmation: false,
            meeting_summary: meeting.summary,
            commitments_created: [],
            commitments_updated: [],
            pending_commitments: meeting.commitments || [],
            warnings: [],
          });
          
          await refreshAll();
          if (meeting.client_id) {
            await loadMemory(meeting.client_id);
          }
          showToast("Transcript successfully reprocessed.");
        } else if (meeting.status === 'client_identification_required') {
          clearInterval(pollInterval);
          state.pendingConfirmationMeetingId = meetingId;
          els.newClientName.value = meeting.suggested_name || "";
          els.confirmPanel.classList.remove("hidden");
          await refreshAll();
          showToast("Client identification required.");
        } else if (meeting.status === 'manual_review_required' || meeting.status === 'failed') {
          clearInterval(pollInterval);
          els.editTranscriptPanel.classList.remove("hidden");
          els.processResult.innerHTML = '<span class="muted">Reprocessing failed again. Please check your text.</span>';
          showToast("Failed to process notes.", true);
        }
      }
    } catch (err) {
      console.error("Polling error:", err);
    }
  }, 2000);
}

function bindEvents() {
  els.topClientSelect.addEventListener("change", (e) => {
    const val = e.target.value;
    if (val) {
      state.selectedClientId = parseInt(val, 10);
      loadMemory().catch((err) => showToast(err.message, true));
    } else {
      state.selectedClientId = null;
      els.memoryContent.innerHTML = `<div class="empty-state">Select a client to view instant context.</div>`;
      els.askClientSection.classList.add("hidden");
    }
    updateMetrics();
  });

  els.saveTranscriptBtn.addEventListener("click", () =>
    withLoading(els.saveTranscriptBtn, "Saving...", () => saveTranscript()).catch((err) => {
      showToast(err.message, true);
      els.editTranscriptPanel.classList.remove("hidden");
      els.processResult.innerHTML = '<span class="muted">Reprocessing failed. Please try again.</span>';
    })
  );

  els.toggleKey.addEventListener("click", () => {
    els.apiKey.type = els.apiKey.type === "password" ? "text" : "password";
  });
  els.processNotes.addEventListener("click", () =>
    withLoading(els.processNotes, "Processing…", () => processNotes()).catch((err) => showToast(err.message, true))
  );
  els.confirmClient.addEventListener("click", () =>
    withLoading(els.confirmClient, "Confirming…", () => confirmClient()).catch((err) => showToast(err.message, true))
  );
  els.loadSelectedMemory.addEventListener("click", () =>
    withLoading(els.loadSelectedMemory, "Loading…", () => loadMemory()).catch((err) => showToast(err.message, true))
  );
  els.commitmentFilter.addEventListener("change", () => loadCommitments().catch((err) => showToast(err.message, true)));
  let askAiRec = null;
  if ('webkitSpeechRecognition' in window) {
    askAiRec = new webkitSpeechRecognition();
    askAiRec.continuous = false;
    askAiRec.interimResults = false;
    askAiRec.lang = 'en-US';
    askAiRec.onresult = (e) => {
      els.askClientInput.value = e.results[0][0].transcript;
      els.askClientInput.placeholder = 'Ask AI about this client...';
      els.askClientBtn.click();
    };
    askAiRec.onerror = (e) => {
      console.error(e);
      els.askClientInput.placeholder = 'Ask AI about this client...';
    };
    askAiRec.onend = () => {
      els.askClientInput.placeholder = 'Ask AI about this client...';
    };
  }

  const askClientVoiceBtn = document.querySelector('#askClientVoiceBtn');
  if (askClientVoiceBtn) {
    askClientVoiceBtn.addEventListener('click', () => {
      if (askAiRec) {
        els.askClientInput.value = '';
        els.askClientInput.placeholder = 'Listening...';
        askAiRec.start();
      } else {
        alert('Voice recognition not supported in this browser.');
      }
    });
  }

  els.askClientBtn.addEventListener("click", () =>
    withLoading(els.askClientBtn, "Asking…", () => askClient()).catch((err) => showToast(err.message, true))
  );
  els.askClientInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      els.askClientBtn.click();
    }
  });

  els.settingsBtn.addEventListener("click", openSettings);
  els.closeSettingsBtn.addEventListener("click", closeSettings);
  els.saveSettingsBtn.addEventListener("click", () =>
    withLoading(els.saveSettingsBtn, "Saving…", () => saveSettings())
  );
  els.settingsModal.addEventListener("click", (e) => {
    if (e.target === els.settingsModal) closeSettings();
  });

  // --- Audio Upload Events ---
  els.tabTextBtn.addEventListener("click", () => {
    els.tabTextBtn.classList.add("active");
    els.tabAudioBtn.classList.remove("active");
    const tabLiveBtn = document.getElementById("tabLiveBtn");
    if (tabLiveBtn) tabLiveBtn.classList.remove("active");

    els.viewText.classList.add("active");
    els.viewText.classList.remove("hidden");
    els.viewText.style.display = ""; // Fix inline style issue
    
    els.viewAudio.classList.remove("active");
    els.viewAudio.classList.add("hidden");
    
    const viewLive = document.getElementById("viewLive");
    if (viewLive) viewLive.style.display = "none";
  });
  
  els.tabAudioBtn.addEventListener("click", () => {
    els.tabAudioBtn.classList.add("active");
    els.tabTextBtn.classList.remove("active");
    const tabLiveBtn = document.getElementById("tabLiveBtn");
    if (tabLiveBtn) tabLiveBtn.classList.remove("active");

    els.viewAudio.classList.add("active");
    els.viewAudio.classList.remove("hidden");
    els.viewAudio.style.display = ""; // Fix inline style issue

    els.viewText.classList.remove("active");
    els.viewText.classList.add("hidden");

    const viewLive = document.getElementById("viewLive");
    if (viewLive) viewLive.style.display = "none";
  });

  els.audioFileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) {
      els.uploadFileName.textContent = file.name;
      els.processAudio.disabled = false;
    } else {
      els.uploadFileName.textContent = "Click to select audio file";
      els.processAudio.disabled = true;
    }
  });

  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    els.uploadBox.addEventListener(eventName, preventDefaults, false);
  });
  
  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ['dragenter', 'dragover'].forEach(eventName => {
    els.uploadBox.addEventListener(eventName, () => els.uploadBox.classList.add('dragover'), false);
  });
  
  ['dragleave', 'drop'].forEach(eventName => {
    els.uploadBox.addEventListener(eventName, () => els.uploadBox.classList.remove('dragover'), false);
  });
  
  els.uploadBox.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if(files.length > 0) {
      els.audioFileInput.files = files;
      els.audioFileInput.dispatchEvent(new Event('change'));
    }
  });

  els.processAudio.addEventListener("click", () => {
    processAudio().catch((err) => {
      showToast(err.message, true);
      els.processAudio.disabled = false;
      els.processAudio.textContent = "Upload & Process";
      els.audioStatusBox.classList.add("hidden");
    });
  });




  els.commitmentRows.addEventListener("click", (event) => {
    const button = event.target.closest("[data-commitment-id]");
    if (!button) return;
    updateCommitmentStatus(Number(button.dataset.commitmentId), button.dataset.nextStatus).catch((err) =>
      showToast(err.message, true)
    );
  });
}

async function processAudio() {
  const file = els.audioFileInput.files[0];
  if (!file) {
    throw new Error("Please select an audio file first.");
  }
  
  if (file.size > 50 * 1024 * 1024) {
    throw new Error("File is too large. Maximum size is 50MB.");
  }

  const dateValue = els.meetingDateAudio.value;
  if (!dateValue) {
    throw new Error("Please select a meeting date.");
  }

  els.processAudio.disabled = true;
  els.editTranscriptPanel.classList.add("hidden");
  els.processAudio.textContent = "Uploading...";
  els.audioStatusBox.classList.remove("hidden");
  els.audioStatusText.textContent = "Uploading...";
  els.audioStatusDetails.textContent = "Please wait while the file is sent to the server.";
  
  const formData = new FormData();
  formData.append("file", file);
  formData.append("meeting_date", dateValue);
  
  const knownClientId = els.knownClient ? els.knownClient.value : "";
  if (knownClientId) {
    formData.append("known_client_id", knownClientId);
  }

  try {
    const response = await fetch("/api/v1/audio/upload", {
      method: "POST",
      headers: {
        "X-API-Key": apiKey(),
      },
      body: formData,
    });
    
    if (!response.ok) {
      let detail = `Upload failed with ${response.status}`;
      try {
        const payload = await response.json();
        detail = payload.detail || detail;
      } catch {
        detail = response.statusText || detail;
      }
      throw new Error(detail);
    }
    
    const result = await response.json();
    
    els.audioStatusText.textContent = "Audio Uploaded & Queued!";
    els.audioStatusDetails.textContent = `Meeting ID: ${result.meeting_id} is now ${result.status}. The AI is processing it in the background. Please wait...`;
    
    // Clear input
    els.audioFileInput.value = "";
    els.uploadFileName.textContent = "Click to select audio file";
    els.processAudio.textContent = "Upload & Process";
    
    showToast("Audio queued for processing.");
    
    // Polling loop
    const meetingId = result.meeting_id;
    const pollInterval = setInterval(async () => {
      try {
        const meetingResponse = await fetch(`/api/v1/meeting-notes/${meetingId}`, {
          headers: { "X-API-Key": apiKey() }
        });
        if (meetingResponse.ok) {
          const meeting = await meetingResponse.json();
          if (meeting.status === 'processed') {
            clearInterval(pollInterval);
            els.audioStatusText.textContent = "Audio Processed!";
            els.audioStatusDetails.textContent = "Processing complete. Your summary and follow-ups are shown below.";
            els.processAudio.disabled = false;

            // The upload endpoint returns immediately, so render the result
            // from the completed polling response rather than leaving the
            // pasted-note result card blank.
            renderProcessResult({
              meeting_id: meeting.id,
              client_status: meeting.client_identification_status || "identified",
              client_id: meeting.client_id,
              requires_client_confirmation: false,
              meeting_summary: meeting.summary,
              commitments_created: [],
              commitments_updated: [],
              pending_commitments: meeting.commitments || [],
              warnings: [],
            });
            
            await refreshAll();
            if (meeting.client_id) {
              await loadMemory(meeting.client_id);
            }
          } else if (meeting.status === 'client_identification_required') {
            clearInterval(pollInterval);
            els.audioStatusText.textContent = "Client Identification Required!";
            els.audioStatusDetails.textContent = "Please confirm the client name to continue.";
            els.processAudio.disabled = false;
            
            state.pendingConfirmationMeetingId = meetingId;
            els.newClientName.value = meeting.suggested_name || "";
            els.confirmPanel.classList.remove("hidden");
            await refreshAll();
          } else if (meeting.status === 'manual_review_required' || meeting.status === 'failed') {
            clearInterval(pollInterval);
            els.audioStatusText.textContent = "Audio Needs Review";
            els.audioStatusDetails.textContent = "PHILIXA could not detect usable speech or safely create a summary. Check the recording and try again.";
            els.processAudio.disabled = false;
            els.editTranscriptText.value = meeting.raw_notes || "";
            els.editTranscriptPanel.dataset.meetingId = meeting.id;
            els.editTranscriptPanel.classList.remove("hidden");
            renderProcessResult({
              meeting_id: meeting.id,
              client_status: "manual review required",
              client_id: meeting.client_id,
              requires_client_confirmation: false,
              meeting_summary: meeting.summary,
              commitments_created: [],
              commitments_updated: [],
              pending_commitments: [],
              warnings: ["No usable meeting summary or follow-ups were saved."],
            });
            showToast("Audio transcript needs manual review.", true);
          }
        }
      } catch (err) {
        console.error("Polling error", err);
      }
    }, 5000);
    
  } catch (error) {
    throw error;
  }
}

async function init() {
  els.meetingDate.value = todayIso();
  if (els.meetingDateAudio) els.meetingDateAudio.value = todayIso();
  bindEvents();
  await refreshAll();
  if (state.selectedClientId) {
    await loadMemory(state.selectedClientId);
  }
}

// =============================================================================
// DAY 12: LIVE TRANSCRIPTION
// =============================================================================

// --- State ---
let liveWs = null;
let audioContext = null;
let audioStream = null;
let workletNode = null;
let liveTranscript = "";
let isLiveRecording = false;
let _liveApiKey = "";
let _liveSampleRate = 16000;

// --- Start Live Recording ---
async function startLiveRecording(diarize = false) {
  if (isLiveRecording) return;

  try {
    // Step 1: Mic permission + WebRTC noise suppression
    audioStream = await navigator.mediaDevices.getUserMedia({
      audio: {
        channelCount: 1,
        echoCancellation: true,    // WebRTC built-in noise suppression
        noiseSuppression: true,    // AC / fan noise fix
        autoGainControl: true,
        // FIX 3: sampleRate hardcode NAHI — browser ka default lene do
      },
    });

    // FIX 3: Browser ka actual sample rate detect karo
    audioContext = new AudioContext();
    _liveSampleRate = audioContext.sampleRate;
    console.log(`[Live] Browser sample rate: ${_liveSampleRate}Hz`);

    // FIX 2: try/catch — silent fail nahi hoga, user ko batao
    try {
      await audioContext.audioWorklet.addModule("/static/pcm-processor.js");
    } catch (err) {
      console.error("[Live] AudioWorklet load failed:", err);
      showToast("❌ Audio processor load nahi hua. Page refresh karo.", true);
      audioContext.close();
      audioContext = null;
      return;
    }

    const source = audioContext.createMediaStreamSource(audioStream);
    workletNode = new AudioWorkletNode(audioContext, "pcm-processor");

    // Step 2: WebSocket connect karo
    _liveApiKey = document.getElementById("apiKey").value;
    connectLiveWebSocket(_liveApiKey, _liveSampleRate, diarize);

    // Step 3: AudioWorklet → WebSocket pipeline
    workletNode.port.onmessage = (event) => {
      if (liveWs?.readyState === WebSocket.OPEN) {
        liveWs.send(event.data); // Raw Int16 binary — zero encoding overhead
      }
    };

    // Step 4: Audio graph connect karo
    source.connect(workletNode);
    workletNode.connect(audioContext.destination);

    isLiveRecording = true;
    updateLiveUI("recording");
  } catch (err) {
    console.error("[Live] Recording start failed:", err);
    updateLiveUI("error", err.message);
  }
}

// Addition B: Auto-reconnect on disconnect (2026 network drop fix)
function connectLiveWebSocket(apiKey, sampleRate, diarize = false) {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/api/v1/live/transcribe?api_key=${apiKey}&sample_rate=${sampleRate}&diarize=${diarize}`;
  liveWs = new WebSocket(wsUrl);
  liveWs.binaryType = "arraybuffer";

  liveWs.onopen = () => {
    console.log("[Live] WebSocket connected.");
    updateLiveUI("recording");
  };

  liveWs.onmessage = (event) => {
    const data = JSON.parse(event.data);

    // Server processing shuru — UI update karo
    if (data.action === "processing") {
      const statusEl = document.getElementById("liveStatusText");
      if (statusEl) statusEl.textContent = "⏳ Processing audio...";
      return;
    }

    // Stop signal confirmed — final transcript ready
    if (data.action === "stopped") {
      if (liveWs) liveWs.close(1000, "Clean close after stop");
      liveWs = null;
      updateLiveUI("stopped");

      // Final transcript → Paste Notes tab mein daalo
      if (data.confirmed && data.confirmed.trim()) {
        const rawNotesEl = document.getElementById("rawNotes");
        if (rawNotesEl) rawNotesEl.value = data.confirmed.trim();
        const tabTextBtn = document.getElementById("tabTextBtn");
        if (tabTextBtn) tabTextBtn.click();
        showToast("✅ Transcript ready! Review and click Process Notes.");
      } else {
        showToast("⚠️ No audio recorded or transcription failed. Please try again.", true);
      }
    }
  };


  // Addition B: Auto-reconnect agar network drop ho
  liveWs.onclose = (event) => {
    console.log(`[Live] WebSocket closed (code: ${event.code}).`);
    if (isLiveRecording && event.code !== 1000) {
      // 1000 = clean user-initiated close — reconnect mat karo
      console.log("[Live] Auto-reconnecting in 2s...");
      setTimeout(() => {
        if (isLiveRecording) {
          connectLiveWebSocket(apiKey, sampleRate, diarize);
        }
      }, 2000);
    }
  };

  liveWs.onerror = (err) => {
    console.error("[Live] WebSocket error:", err);
  };
}

// --- Stop Live Recording ---
function stopLiveRecording() {
  isLiveRecording = false;

  // Audio graph cleanup
  workletNode?.disconnect();
  audioContext?.close();
  audioStream?.getTracks().forEach((t) => t.stop());

  workletNode = null;
  audioContext = null;
  audioStream = null;

  if (liveWs?.readyState === WebSocket.OPEN) {
    // Send stop signal to flush backend buffer immediately
    liveWs.send(JSON.stringify({ action: "stop" }));
    const stopBtn = document.getElementById("stopLiveBtn");
    if (stopBtn) {
      stopBtn.textContent = "Saving...";
      stopBtn.disabled = true;
    }
  } else {
    liveWs = null;
    updateLiveUI("stopped");
  }
}

// --- UI State Helper ---
function updateLiveUI(state, message = "") {
  const states = {
    recording: { text: "🔴 Recording...", startDisabled: true,  stopDisabled: false },
    stopped:   { text: "⏸ Ready",        startDisabled: false, stopDisabled: true  },
    error:     { text: `❌ ${message}`,   startDisabled: false, stopDisabled: true  },
  };
  const s = states[state] || states.stopped;
  const statusEl = document.getElementById("liveStatusText");
  const soloBtn    = document.getElementById("startSoloBtn");
  const meetingBtn = document.getElementById("startMeetingBtn");
  const stopBtn    = document.getElementById("stopLiveBtn");
  if (statusEl) statusEl.textContent = s.text;
  if (soloBtn)    soloBtn.disabled    = s.startDisabled;
  if (meetingBtn) meetingBtn.disabled = s.startDisabled;
  if (stopBtn) {
    stopBtn.disabled = s.stopDisabled;
    if (state === "stopped") stopBtn.textContent = "Stop & Save";
  }
}

// FIX 6: Tab switching event listener — existing tab pattern ke saath integrate
document.addEventListener("DOMContentLoaded", () => {
  const tabLiveBtn = document.getElementById("tabLiveBtn");
  if (!tabLiveBtn) return;

  tabLiveBtn.addEventListener("click", () => {
    // Existing tabs hide karo
    document.getElementById("viewText")?.setAttribute("style", "display:none");
    document.getElementById("viewAudio")?.setAttribute("style", "display:none");
    // Live view show karo
    const liveView = document.getElementById("viewLive");
    if (liveView) liveView.style.display = "block";
    // Active class update
    document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
    tabLiveBtn.classList.add("active");
  });
});

// =============================================================================
// END DAY 12
// =============================================================================

// =============================================================================
// Theme Toggle Logic
// =============================================================================
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.querySelector("#themeToggleBtn");
  if (!btn) return;

  // Check local storage for saved theme
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    document.body.classList.add("dark-theme");
    btn.textContent = "☀️";
  }

  btn.addEventListener("click", () => {
    document.body.classList.toggle("dark-theme");
    if (document.body.classList.contains("dark-theme")) {
      localStorage.setItem("theme", "dark");
      btn.textContent = "☀️";
    } else {
      localStorage.setItem("theme", "light");
      btn.textContent = "🌙";
    }
  });
});

init().catch((err) => showToast(err.message, true));
