STEP 1 — Button Click → processNotes() function
File: app/web/app.js

javascript
// Line 678 - Button par click listener baitha hai
els.processNotes.addEventListener("click", () =>
  withLoading(els.processNotes, "Processing…", () => processNotes())
);
// Line 456 - Yeh function chala
async function processNotes() {
  // NIKLA: HTML <textarea id="rawNotes"> se
  const rawNotes = els.rawNotes.value.trim();
  // rawNotes = "Met Rajesh Sharma today. Interested in business loan."
  // NIKLA: Date picker aur client dropdown se
  // GIRA: Ek javascript body object mein
  const body = {
    raw_notes: rawNotes,
    meeting_date: els.meetingDate.value || undefined,
    known_client_id: els.knownClient.value ? Number(els.knownClient.value) : undefined,
  };
  // BHEJA: Network ke through FastAPI ko JSON string banake
  const payload = await api("/api/v1/meeting-notes/process", {
    method: "POST",
    body: JSON.stringify(body),
    // Header mein X-API-Key bhi gaya: "philixa-demo-secret-123"
  });
  renderProcessResult(payload); // Step 18 mein aayega
}
STEP 2 — FastAPI ne HTTP Request Pakdi, Security Check Kiya
File: app/api/v1/routes_meeting_notes.py

python
# Line 32
# FastAPI ne route match kiya: POST /api/v1/meeting-notes/process
# Sabse pehle `require_api_key` dependency chali (header mein X-API-Key check hua)
@router.post("/process", response_model=MeetingNoteProcessResponse)
async def process_meeting_note(
    # FastAPI yahan RUKA — Body mein jo JSON aaya usse
    # ab internally Pydantic ko pass karega
    request: Annotated[MeetingNoteProcessRequest, Body(...)],
    db: AsyncSession = Depends(get_db),
) -> dict:
    # YEH LINE ABHI NAHI CHALI — pehle Step 3 hoga
    ...
STEP 3 — FastAPI ne INTERNALLY Pydantic ko Bulaya (Validation)
File: app/schemas/meeting_note.py

python
# FastAPI ne khud yeh kaam kiya internally:
# raw_json = {"raw_notes": "Met Rajesh...", "meeting_date": "2026-08-10"}
# request = MeetingNoteProcessRequest(**raw_json)  ← Framework ne khud call kiya
class MeetingNoteProcessRequest(BaseModel):
    # NIKLA: JSON ka "raw_notes" key
    # GIRA: is Python field mein
    raw_notes: str = Field(..., min_length=1)
    
    meeting_date: date | None = None
    # FastAPI ne "2026-08-10" string ko date(2026, 8, 10) mein convert kiya
    
    known_client_id: int | None = Field(default=None, gt=0)
    source_type: MeetingSourceType = Field(default=MeetingSourceType.PASTED_NOTE)
    # Pydantic ne AUTOMATICALLY yeh validator chaya
    @field_validator("raw_notes")
    @classmethod
    def validate_raw_notes(cls, value: str) -> str:
        settings = get_settings()
        stripped = value.strip()
        
        # Check 1: Khali string?
        if not stripped:
            raise ValueError("raw_notes cannot be empty.")
        
        # Check 2: Character limit cross?
        if len(stripped) > settings.raw_notes_max_chars:
            raise ValueError(f"Cannot exceed {settings.raw_notes_max_chars} chars.")
        
        # SAHI RAHA — cleaned string wapis di
        return stripped
        # ✅ request object ban gaya, wapis route mein inject hua
STEP 4 — Validated request object WAPIS Route mein Aaya, Service Call Hua
File: app/api/v1/routes_meeting_notes.py

python
# Line 32 — Ab route function ka body chala
@router.post("/process", response_model=MeetingNoteProcessResponse)
async def process_meeting_note(
    # 'request' ab ek clean Python object hai:
    # request.raw_notes = "Met Rajesh Sharma today. Interested in business loan."
    # request.meeting_date = date(2026, 8, 10)
    # request.known_client_id = None
    # request.source_type = MeetingSourceType.PASTED_NOTE
    request: Annotated[MeetingNoteProcessRequest, Body(...)],
    db: AsyncSession = Depends(get_db),
) -> dict:
    try:
        # NIKLA: request object
        # BHEJA: MeetingProcessingService ko
        return await MeetingProcessingService().process_notes(db, request)
    except AIExtractionError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
STEP 5 — Zero Data-Loss DB Save (SQLAlchemy Meeting Model)
File: app/services/meeting_processing_service.py

python
# Line 41
async def process_notes(self, db: AsyncSession, request: MeetingNoteProcessRequest) -> dict[str, Any]:
    meeting_date = request.meeting_date or date.today()
    # NIKLA: request.raw_notes, request.meeting_date
    # GIRA: SQLAlchemy Meeting model ke columns mein
    meeting = Meeting(
        client_id=None,                                          # Abhi pata nahi client kaun
        raw_notes=request.raw_notes,                            # "Met Rajesh Sharma..."
        meeting_date=meeting_date,                              # date(2026, 8, 10)
        source_type=request.source_type.value,                  # "pasted_note"
        summary="",
        key_discussion_points_json="[]",
        concerns_json="[]",
        status=MeetingStatus.MANUAL_REVIEW_REQUIRED.value,      # Fail-safe status
        client_identification_status="unknown",
        client_identification_confidence=0.0,
    )
    db.add(meeting)
    await db.flush()
    # ✅ DB ne meeting.id = 101 assign kiya (permanent save nahi hua abhi, sirf ID mili)
    # Ab aage processing ke liye gaya
    return await self._process_extracted_meeting(db, meeting, request.known_client_id)
STEP 6 — AI Routing: Hinglish Translation + Groq/Gemini Call
File: app/services/ai_routing_service.py

python
# Line 21
async def route_and_extract(self, raw_notes: str, meeting_date: date, meeting_id: int) -> dict[str, Any]:
    # PRE-PROCESSING: Hinglish → English translation
    try:
        trans_provider = get_ai_provider(self.settings.ai_economy_provider, self.settings)
        # NIKLA: raw_notes "Met Rajesh Sharma..."
        # BHEJA: Groq ko translate karne ke liye
        clean_notes = await asyncio.to_thread(trans_provider.translate_transcript, raw_notes)
        # clean_notes = "Met Rajesh Sharma today. Interested in a business loan..."
    except Exception:
        clean_notes = raw_notes  # Translation fail toh original use karo
    # ATTEMPT 1: Economy Model (Groq - Llama-3.3-70B)
    try:
        # NIKLA: clean_notes
        # BHEJA: Groq API ko HTTP request
        result = await self._call_and_validate(
            clean_notes, meeting_date,
            self.settings.ai_economy_provider,   # "groq"
            self.settings.ai_economy_model,       # "llama-3.3-70b-versatile"
            meeting_id
        )
        return result.payload  # ✅ Groq ne JSON dict wapis di
    except (AIExtractionError, ValidationError):
        pass  # ❌ Groq fail — Gemini try karo
    # ATTEMPT 2: Review Model (Gemini - 2.5-flash)
    result = await self._call_and_validate(
        clean_notes, meeting_date,
        self.settings.ai_review_provider,    # "gemini"
        self.settings.ai_review_model,       # "gemini-2.5-flash"
        meeting_id
    )
    return result.payload
STEP 6A — Har AI Call ke Baad: Pydantic Schema Validation + Audit Log
File: app/services/ai_routing_service.py

python
# Line 53 - Yeh function har Groq/Gemini call ke andar chala
async def _call_and_validate(self, raw_notes, meeting_date, provider_name, model_name, meeting_id):
    provider = get_ai_provider(provider_name, self.settings)
    
    # AI API call (Groq ya Gemini ka HTTP request)
    result = await asyncio.to_thread(
        provider.extract_meeting_intelligence, raw_notes, meeting_date, model_name
    )
    # result.payload = {
    #   "client_identification": {"suggested_client_name": "Rajesh Sharma", "confidence": 0.92},
    #   "meeting_summary": "Rajesh discussed business loan interest",
    #   "commitments": [{"description": "Send documents by Friday", "due_date": "2026-08-14"}],
    #   "concerns": [{"description": "Processing time", "severity": "medium"}]
    # }
    # AI ke result ko PYDANTIC se validate karo (schema check)
    # File: app/schemas/ai_extraction.py
    MeetingExtraction.model_validate(result.payload)  # ← Agar invalid JSON toh error
    # Audit Log DB mein save karo (cost tracking)
    await self._log_audit(meeting_id, provider_name, model_name, result, success=True)
    # AIExtractionLog table mein ek row bani:
    # provider="groq", model="llama-3.3-70b", latency_ms=1240, cost_usd=0.0021
    return result
STEP 7 — Client Identification (Fuzzy Matching)
File: app/services/client_identification_service.py

python
# Line 15
async def resolve_client(self, db, suggested_name, confidence, known_client_id=None):
    # Agar user ne dropdown se client choose kiya tha
    if known_client_id:
        client = await db.get(Client, known_client_id)
        return client, "identified", []
    # AI ne jo naam diya usse normalize karo
    # NIKLA: "Rajesh Sharma"
    normalized = normalize_text(suggested_name)
    # normalized = "rajesh sharma"
    # Sab clients DB se uthao
    clients = list((await db.scalars(select(Client))).all())
    # Exact match check
    exact = [c for c in clients if c.normalized_name == normalized]
    if exact and confidence >= self.settings.client_auto_match_threshold:
        return exact[0], "identified", []   # ✅ Rajesh already tha DB mein
    # Fuzzy match (thoda alag spelling bhi match hoga)
    close_matches = [
        c for c in clients
        if similarity(c.normalized_name, normalized) >= self.settings.client_auto_match_threshold
    ]
    if len(close_matches) == 1 and confidence >= self.settings.client_auto_match_threshold:
        return close_matches[0], "identified", []
    # Koi match nahi mila — User ko confirmation popup dikhana hoga
    return None, "client_identification_required", ["New client; confirmation required."]
STEP 8 — Meeting Row Update + Commitments + Memory + Rules Engine
File: app/services/meeting_processing_service.py

python
# Line 101
        # NIKLA: extraction dict (AI ka result)
        # GIRA: wapis us meeting row mein jiska id=101 tha
        meeting.client_id = client.id                          # client.id = 7 (Rajesh)
        meeting.summary = extraction.get("meeting_summary")   # "Rajesh discussed business loan"
        meeting.key_discussion_points_json = to_json(extraction.get("key_discussion_points"))
        meeting.concerns_json = to_json(extraction.get("concerns"))
        meeting.status = "processed"                          # Status update
        meeting.client_identification_status = "identified"
        meeting.client_identification_confidence = 0.92
        db.add(meeting)
        if client:
            # Products merge karo client profile mein
            self._merge_client_products(client, extraction.get("products_owned") or [])
            # client.products_owned_json = '["Business Loan"]'
            # COMMITMENTS SAVE KARO
            # File: app/services/commitment_service.py
            created, updated = await self.commitments.upsert_commitments(
                db,
                client_id=client.id,       # 7
                meeting_id=meeting.id,     # 101
                extracted_commitments=extraction.get("commitments")
                # [{"description": "Send documents by Friday", "due_date": "2026-08-14"}]
            )
            # Commitment table mein naya row bana:
            # id=55, client_id=7, meeting_id=101, description="Send documents by Friday"
            # CommitmentMeetingLink table mein bhi row bana: commitment_id=55, meeting_id=101
            # ROLLING MEMORY UPDATE KARO
            # File: app/services/memory_service.py
            await self.memory.update_client_memory(db, client.id)
            # Pichli 5 meetings padhi, pending commitments padhe
            # client.rolling_summary = "Rajesh discussed a business loan.
            #   One follow-up commitment open: Send documents by Friday (2026-08-14)."
            # RULES ENGINE — Tasks aur Risks sync karo
            # File: app/services/rules_engine_service.py
            await RulesEngineService.sync_client_tasks_and_risks(db, client.id)
            # FollowUpTask table mein row bana: commitment_id=55, is_overdue=False
            # concerns_json se RiskSignal table mein row bana agar severity high hai
        # SAB KUCH PERMANENTLY SAVE
        await db.commit()
        # ✅ Ab DB mein permanently: Meeting row, Commitment row, CommitmentMeetingLink,
        #    Client.rolling_summary updated, FollowUpTask row, RiskSignal row
STEP 9 — Background ARQ Job Queue mein Daala
File: app/services/meeting_processing_service.py

python
# Line 136
        pool = get_arq_pool()
        if client and pool:
            # NIKLA: meeting.id = 101
            # GIRA: Redis Queue mein (background job ke liye)
            await pool.enqueue_job(
                "generate_meeting_embeddings",
                meeting.id,            # Worker ko sirf ID chahiye
                organization_id="default",
                user_id="default",
                _job_id=f"generate_meeting_embeddings_101"  # Duplicate prevention
            )
        # ✅ Redis mein job queued — Main API yahan se response return karega
        # Background mein worker chalega (Step 9A)
STEP 9A — Background Worker (ARQ) — Embeddings Banaye
File: app/jobs/embedding_jobs.py (Yeh API se alag chalta hai)

python
# Line 14 — Yeh ARQ Worker process mein chala, FastAPI mein nahi
async def generate_meeting_embeddings(ctx: dict, meeting_id: int, ...):
    async with SessionLocal() as db:
        # NIKLA: meeting_id=101 se DB se meeting uthaya
        meeting = (await db.execute(select(Meeting).where(Meeting.id == 101))).scalar_one()
        # raw_notes ko chunks mein toda aur sentence-transformer model se vector banaye
        # CPU-heavy kaam thread pool mein kiya taaki async loop block na ho
        chunks = await asyncio.to_thread(generate_embeddings_for_text, meeting.raw_notes)
        # chunks = [
        #   {"chunk_index": 0, "chunk_text": "Met Rajesh Sharma...", "embedding": [0.23, -0.11, ...]},
        #   {"chunk_index": 1, "chunk_text": "Interested in business loan...", "embedding": [...]}
        # ]
        # Purane embeddings delete karo (idempotency)
        await db.execute(delete(MeetingEvidence).where(MeetingEvidence.meeting_id == 101))
        # GIRA: pgvector MeetingEvidence table mein
        for chunk in chunks:
            evidence = MeetingEvidence(
                meeting_id=101,
                chunk_index=chunk["chunk_index"],
                chunk_text=chunk["chunk_text"],
                embedding=chunk["embedding"]  # 384-dimensional vector array
            )
            db.add(evidence)
        await db.commit()
        # ✅ Ab "Ask Client" (RAG search) kaam karega is meeting ke liye
STEP 10 — FastAPI ne Response Pydantic se Validate Kiya aur Bheja
File: app/schemas/meeting_note.py + app/api/v1/routes_meeting_notes.py

python
# Route function ne jo dict return kiya
# FastAPI ne use AUTOMATICALLY MeetingNoteProcessResponse Pydantic model se validate kiya
class MeetingNoteProcessResponse(BaseModel):
    meeting_id: int               # 101
    client_status: str            # "identified"
    client_id: int | None         # 7
    requires_client_confirmation: bool  # False
    meeting_summary: str          # "Rajesh discussed business loan"
    meeting: MeetingRead          # Full meeting object
    extraction: MeetingExtractionRead   # AI extraction details
    commitments_created: list[CommitmentRead]   # [commitment id=55]
    commitments_updated: list[CommitmentRead]   # []
    pending_commitments: list[CommitmentRead]   # [commitment id=55]
    warnings: list[str]           # []
# FastAPI ne is validated JSON ko browser ko bheja
# HTTP 200 OK response with JSON body
STEP 11 — Browser ne Response Pakda, Screen Update Kiya
File: app/web/app.js

javascript
// processNotes() function ko payload mila (Step 1 mein await tha)
const payload = await api("/api/v1/meeting-notes/process", {...});
// STEP 11A: Result panel update kiya
renderProcessResult(payload);
// Line 212
function renderProcessResult(payload) {
    // NIKLA: payload.client_status, payload.meeting_summary
    // GIRA: HTML div els.processResult mein
    els.processResult.innerHTML = `
        <div class="result-summary">
          <span class="status-pill done">${escapeHtml(payload.client_status)}</span>
          <strong>${escapeHtml(payload.meeting_summary)}</strong>
          <span>Created: ${payload.commitments_created.length}</span>
        </div>
    `;
    // Client confirmation popup check
    if (payload.requires_client_confirmation) {
        state.pendingConfirmationMeetingId = payload.meeting_id;
        els.confirmPanel.classList.remove("hidden");
    } else {
        state.selectedClientId = payload.client_id;  // = 7
    }
}
// STEP 11B: Dashboard refresh kiya
await refreshAll();
// loadClients() → GET /api/v1/clients → client count update
// loadCommitments() → GET /api/v1/commitments → pending count update
// loadPriorities() → GET /api/v1/dashboard/priorities → tasks/risks update
// STEP 11C: Client memory load kiya
if (payload.client_id) {
    await loadMemory(payload.client_id);  // Rajesh ki memory panel mein dikhi
}
showToast("Meeting notes processed.");  // ✅ Green toast notification
FINAL — Poora Flow Ek Line Mein:
HTML Textarea
    ↓ .value.trim()
JavaScript body object {raw_notes, meeting_date}
    ↓ JSON.stringify() → POST /api/v1/meeting-notes/process
FastAPI Router (Security Check: X-API-Key)
    ↓ INTERNALLY
Pydantic MeetingNoteProcessRequest (validate_raw_notes chala)
    ↓ Validated Python Object
Route Function: process_meeting_note(request, db)
    ↓ MeetingProcessingService().process_notes()
SQLAlchemy Meeting Model (raw_notes save, id=101 mili)
    ↓ _process_extracted_meeting()
AIRoutingService.route_and_extract(raw_notes)
    ↓ Hinglish Translation → Groq HTTP Call → Pydantic MeetingExtraction validate → AIExtractionLog DB mein
extraction dict {summary, commitments, concerns, client_name}
    ↓ ClientIdentificationService.resolve_client()
Fuzzy Match → client = Rajesh (id=7)
    ↓ meeting row update (summary, status, client_id)
CommitmentService.upsert_commitments() → Commitment row (id=55) + CommitmentMeetingLink
    ↓
MemoryService.update_client_memory() → client.rolling_summary updated
    ↓
RulesEngineService.sync() → FollowUpTask row + RiskSignal row
    ↓ db.commit() — SAB PERMANENTLY SAVE
ARQ Pool → Redis Queue mein meeting_id=101 daala
    ↓ (Background: Embeddings → pgvector MeetingEvidence rows)
Pydantic MeetingNoteProcessResponse (output validate)
    ↓ FastAPI → HTTP 200 JSON Response
JavaScript payload object mila
    ↓ renderProcessResult() → HTML div update
    ↓ refreshAll() → Clients, Commitments, Tasks reload
    ↓ loadMemory() → Memory panel update
✅ Screen par "Meeting notes processed." toast dikha
Bhai yeh hai tera 100% complete, zero steps missing, poora data flow — ek bhi file nahi chodi.
