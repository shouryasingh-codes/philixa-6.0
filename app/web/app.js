const state = {
  clients: [],
  commitments: [],
  priorities: { tasks: [], risks: [] },
  selectedClientId: null,
  pendingConfirmationMeetingId: null,
};

const els = {
  apiKey: document.querySelector("#apiKey"),
  toggleKey: document.querySelector("#toggleKey"),
  healthDot: document.querySelector("#healthDot"),
  healthText: document.querySelector("#healthText"),
  refreshAll: document.querySelector("#refreshAll"),
  refreshClients: document.querySelector("#refreshClients"),
  clientCount: document.querySelector("#clientCount"),
  pendingCount: document.querySelector("#pendingCount"),
  selectedClientLabel: document.querySelector("#selectedClientLabel"),
  rawNotes: document.querySelector("#rawNotes"),
  meetingDate: document.querySelector("#meetingDate"),
  knownClient: document.querySelector("#knownClient"),
  processNotes: document.querySelector("#processNotes"),
  processResult: document.querySelector("#processResult"),
  confirmPanel: document.querySelector("#confirmPanel"),
  confirmClientSelect: document.querySelector("#confirmClientSelect"),
  newClientName: document.querySelector("#newClientName"),
  confirmClient: document.querySelector("#confirmClient"),
  clientList: document.querySelector("#clientList"),
  loadSelectedMemory: document.querySelector("#loadSelectedMemory"),
  memoryContent: document.querySelector("#memoryContent"),
  commitmentFilter: document.querySelector("#commitmentFilter"),
  commitmentRows: document.querySelector("#commitmentRows"),
  refreshPriorities: document.querySelector("#refreshPriorities"),
  taskList: document.querySelector("#taskList"),
  riskList: document.querySelector("#riskList"),
  toast: document.querySelector("#toast"),
  askClientSection: document.querySelector("#askClientSection"),
  askClientInput: document.querySelector("#askClientInput"),
  askClientBtn: document.querySelector("#askClientBtn"),
  askClientResult: document.querySelector("#askClientResult"),
  settingsBtn: document.querySelector("#settingsBtn"),
  settingsModal: document.querySelector("#settingsModal"),
  closeSettingsBtn: document.querySelector("#closeSettingsBtn"),
  prefOptIn: document.querySelector("#prefOptIn"),
  prefContact: document.querySelector("#prefContact"),
  prefQuietStart: document.querySelector("#prefQuietStart"),
  prefQuietEnd: document.querySelector("#prefQuietEnd"),
  saveSettingsBtn: document.querySelector("#saveSettingsBtn"),
};

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
  const selected = state.clients.find((client) => client.id === state.selectedClientId);
  els.selectedClientLabel.textContent = selected ? selected.name : "None";
}

function renderClientOptions() {
  const clientOptions = state.clients
    .map((client) => `<option value="${client.id}">${escapeHtml(client.name)}</option>`)
    .join("");
  els.knownClient.innerHTML = `<option value="">Auto identify client</option>${clientOptions}`;
  els.confirmClientSelect.innerHTML = `<option value="">Select existing client</option>${clientOptions}`;
}

function renderClients() {
  if (!state.clients.length) {
    els.clientList.innerHTML = `<span class="muted">No clients yet. Process a clear note to create one.</span>`;
    renderClientOptions();
    updateMetrics();
    return;
  }
  els.clientList.innerHTML = state.clients
    .map((client) => {
      const active = client.id === state.selectedClientId ? " active" : "";
      const preview = client.rolling_summary || client.last_meeting_summary || "No meeting yet";
      return `
        <button class="client-item${active}" type="button" data-client-id="${client.id}">
          <span class="client-copy">
            <strong>${escapeHtml(client.name)}</strong>
            <span class="client-meta">${client.pending_commitments_count} pending - ${escapeHtml(preview)}</span>
          </span>
          <span class="client-actions">
            <span class="status-pill">${client.id}</span>
            <span class="delete-client" title="Delete client" data-delete-client-id="${client.id}">Delete</span>
          </span>
        </button>
      `;
    })
    .join("");
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
          <td>${escapeHtml(item.due_date || item.due_date_text || "Unknown")}</td>
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
      ${commitments.length ? `<ul>${commitments.map((item) => `<li>${escapeHtml(item.description)} - ${escapeHtml(item.due_date || item.due_date_text || "Unknown due date")}</li>`).join("")}</ul>` : `<span class="muted">No pending commitments.</span>`}
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
    els.taskList.innerHTML = `<span class="muted">No overdue or due-today tasks.</span>`;
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
    els.riskList.innerHTML = `<span class="muted">No high-risk signals.</span>`;
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

function bindEvents() {
  els.toggleKey.addEventListener("click", () => {
    els.apiKey.type = els.apiKey.type === "password" ? "text" : "password";
  });
  els.refreshAll.addEventListener("click", () =>
    withLoading(els.refreshAll, "Refreshing…", () => refreshAll()).catch((err) => showToast(err.message, true))
  );
  els.refreshClients.addEventListener("click", () =>
    withLoading(els.refreshClients, "Loading…", () => loadClients()).catch((err) => showToast(err.message, true))
  );
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
  els.refreshPriorities.addEventListener("click", () =>
    withLoading(els.refreshPriorities, "Loading…", () => loadPriorities()).catch((err) => showToast(err.message, true))
  );
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

  els.clientList.addEventListener("click", (event) => {
    const deleteButton = event.target.closest("[data-delete-client-id]");
    if (deleteButton) {
      event.preventDefault();
      event.stopPropagation();
      deleteClient(Number(deleteButton.dataset.deleteClientId)).catch((err) => showToast(err.message, true));
      return;
    }
    const button = event.target.closest("[data-client-id]");
    if (!button) return;
    loadMemory(Number(button.dataset.clientId)).catch((err) => showToast(err.message, true));
  });

  els.commitmentRows.addEventListener("click", (event) => {
    const button = event.target.closest("[data-commitment-id]");
    if (!button) return;
    updateCommitmentStatus(Number(button.dataset.commitmentId), button.dataset.nextStatus).catch((err) =>
      showToast(err.message, true)
    );
  });
}

async function init() {
  els.meetingDate.value = todayIso();
  bindEvents();
  await refreshAll();
  if (state.selectedClientId) {
    await loadMemory(state.selectedClientId);
  }
}

init().catch((err) => showToast(err.message, true));
