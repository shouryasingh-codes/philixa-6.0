# 🧠 Philixa 6.0 — Ultra-Detailed Data Flow
## `POST /api/v1/meeting-notes/process` — Har Byte Ka Safar

> **Scope**: Ek single button click se lekar database mein permanently data save hone tak —
> har function call, har variable transformation, har network hop, har side effect documented hai.

---

## 📌 LEGEND (Padhne se pehle)

| Symbol | Matlab |
|--------|--------|
| `NIKLA` | Data yahan se aaya |
| `GIRA` | Data yahan pada |
| `BHEJA` | Data yahan bheja gaya (network/function) |
| `BADLA` | Data ka format/type change hua |
| `CHEKA` | Validation/check hua |
| `SAVE` | Database mein likha gaya |
| `⚠️` | Failure case — yahan error aa sakti hai |
| `✅` | Success checkpoint |
| `🔴` | Critical path — agar yeh fail hua toh poora request fail |
| `🟡` | Non-critical path — fail hone par fallback hai |

---

## ═══════════════════════════════════════════
## STEP 1 — Browser Event Loop: Button Click → DOM Read → HTTP Request
### File: `app/web/app.js`
## ═══════════════════════════════════════════

### 1.1 — Event Listener Registration (App startup par ek baar)

```
[APP LOAD TIME]
    ↓
document.addEventListener("DOMContentLoaded", init)
    ↓ init() chali
els = {
    processNotes:  document.getElementById("processNotes"),   // <button>
    rawNotes:      document.getElementById("rawNotes"),       // <textarea>
    meetingDate:   document.getElementById("meetingDate"),    // <input type="date">
    knownClient:   document.getElementById("knownClient"),    // <select>
    processResult: document.getElementById("processResult"),  // <div>
    confirmPanel:  document.getElementById("confirmPanel"),   // <div>
}
    ↓
els.processNotes.addEventListener("click", handler)
// Handler registered hua — ab browser is button par click ka wait karega
```

> **Kyun `els` object?** Baar baar `document.getElementById()` call karna slow hota hai.
> `els` ek cache hai — app start par ek baar DOM query, baaki sab time direct access.

---

### 1.2 — User Click → `withLoading()` Wrapper

```
[USER CLICK EVENT FIRE HUA]
    ↓
Browser ne click event queue mein daala
    ↓
JavaScript Event Loop ne uthaya
    ↓
withLoading(els.processNotes, "Processing…", () => processNotes())
```

**`withLoading()` ke andar kya hua:**

```javascript
// withLoading ka internal logic (simplified):
async function withLoading(btn, text, asyncFn) {
    // STEP 1: Button disable karo (double-submit rokne ke liye)
    btn.disabled = true
    const originalText = btn.textContent   // "Process Notes" store kiya
    btn.textContent = text                 // "Processing…" dikhaya
    
    try {
        // STEP 2: Actual async function chalayi (processNotes)
        await asyncFn()                    // ← YEH AWAIT HAI — button tab tak disabled rahega
    } finally {
        // STEP 3: Chahe success ho ya error — button restore karo
        btn.disabled = false
        btn.textContent = originalText     // "Process Notes" wapis
    }
}
```

> **Important side effect:** Jab tak `processNotes()` complete nahi hoti (success ya error),
> tab tak button disabled rahega. Yeh UX protection hai — user accidentally double submit nahi kar sakta.

---

### 1.3 — `processNotes()` — DOM se Data Nikalna

```javascript
async function processNotes() {

    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // READ #1: Textarea se raw text
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // NIKLA: <textarea id="rawNotes"> ka .value property
    // .value = "  Met Rajesh Sharma today. Interested in business loan.  \n"
    // .trim() ne leading/trailing whitespace hataya
    const rawNotes = els.rawNotes.value.trim()
    // rawNotes = "Met Rajesh Sharma today. Interested in business loan."
    // Type: string | ""  ← khali string possible hai (backend validate karega)

    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // READ #2: Date picker
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // els.meetingDate.value = "2026-08-10" (YYYY-MM-DD format — HTML date input ka standard)
    // Agar date nahi choose ki → .value = "" (empty string)
    // `|| undefined` → empty string ko undefined banata hai
    //   WHY?: JSON.stringify({key: undefined}) → key hi serialize nahi hoti
    //   JSON.stringify({key: ""}) → {"key": ""} — yeh galat hoga backend ke liye
    const meeting_date = els.meetingDate.value || undefined
    // meeting_date = "2026-08-10"  OR  undefined

    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // READ #3: Client dropdown
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // els.knownClient.value = "7" (string! — HTML select hamesha string deta hai)
    // Agar koi select nahi kiya → .value = "" (empty string / placeholder option)
    // Number() → "7" ko 7 (integer) mein convert karta hai
    // Ternary: khali string falsy hai → undefined return
    const known_client_id = els.knownClient.value
        ? Number(els.knownClient.value)   // "7" → 7
        : undefined                       // "" → undefined

    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // JAVASCRIPT BODY OBJECT BANA
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    const body = {
        raw_notes: rawNotes,           // string: "Met Rajesh Sharma..."
        meeting_date: meeting_date,    // string: "2026-08-10" | undefined
        known_client_id: known_client_id  // number: 7 | undefined
    }
    // body = { raw_notes: "Met Rajesh Sharma...", meeting_date: "2026-08-10" }
    // (known_client_id field exist hi nahi karti agar undefined — JSON.stringify removes it)
```

---

### 1.4 — `api()` Helper → HTTP Request Construction

```javascript
    // api() ek wrapper function hai fetch() ke upar
    const payload = await api("/api/v1/meeting-notes/process", {
        method: "POST",
        body: JSON.stringify(body),
    })
```

**`api()` helper ke andar kya hua (deep dive):**

```javascript
async function api(path, options = {}) {
    // API_KEY environment/config se aata hai: "philixa-demo-secret-123"
    const response = await fetch(path, {
        ...options,
        headers: {
            "Content-Type": "application/json",   // Server ko bataya: body JSON hai
            "X-API-Key": API_KEY,                 // "philixa-demo-secret-123"
            ...(options.headers || {})
        }
    })
    
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // HTTP Error handling
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    if (!response.ok) {
        // response.ok = false when status >= 400
        const errorData = await response.json().catch(() => ({}))
        // ⚠️ Error throw → withLoading ka finally block button restore karega
        throw new Error(errorData.detail || `HTTP ${response.status}`)
    }
    
    return response.json()  // Response body JSON parse karke return
}
```

**HTTP Request jo actually wire par gaya:**

```http
POST /api/v1/meeting-notes/process HTTP/1.1
Host: localhost:8000
Content-Type: application/json
X-API-Key: philixa-demo-secret-123
Content-Length: 89

{"raw_notes":"Met Rajesh Sharma today. Interested in business loan.","meeting_date":"2026-08-10"}
```

> **Network ke through kya hua:**
> 1. Browser ne TCP connection establish kiya (ya existing connection reuse)
> 2. HTTP request bytes wire par gaye
> 3. `await api(...)` — JavaScript event loop yahan RUKA (suspend hua)
> 4. Browser ne background mein response ka wait kiya (non-blocking)
> 5. Response aane par — event loop ne `processNotes()` ko resume kiya

---

## ═══════════════════════════════════════════
## STEP 2 — FastAPI: Request Receive → Middleware Stack → Security
### File: `app/api/v1/routes_meeting_notes.py` + `app/core/security.py`
## ═══════════════════════════════════════════

### 2.1 — Uvicorn/Starlette ASGI Stack

```
[HTTP Request bytes arrive at server]
    ↓
Uvicorn (ASGI server) — raw bytes ko Python objects mein convert kiya
    ↓
Starlette ASGI app (FastAPI ka base)
    ↓
Middleware Stack (sequential):
    ├── CORSMiddleware       → Origin check (localhost allowed hai)
    ├── GZipMiddleware       → Response compression (request pe nahi)
    └── (Custom middlewares agar koi hain)
    ↓
FastAPI Router — URL match kiya
    Route: POST /api/v1/meeting-notes/process ✅ MATCH
```

---

### 2.2 — Security: `require_api_key` Dependency

```python
# FastAPI pehle SAARI dependencies resolve karta hai
# Route function se pehle

# app/core/security.py
async def require_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    # Header("X-API-Key") = "philixa-demo-secret-123"
    # NIKLA: HTTP header "X-API-Key"
    # CHEKA: Settings mein stored key se match kiya
    
    settings = get_settings()
    # settings.api_key = "philixa-demo-secret-123"  (env var se loaded)
    
    if x_api_key != settings.api_key:
        # ⚠️ 403 Forbidden → Request yahan STOP — Route function kabhi nahi chalega
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )
    # ✅ Key match — dependency successfully resolved
    # FastAPI aage badha
```

> **FastAPI Dependency Injection kaise kaam karta hai:**
> - `Depends(require_api_key)` route par registered hai
> - FastAPI request aane par pehle sabhi `Depends()` resolve karta hai
> - Agar koi dependency fail hui (exception raise ki) → Route function run hi nahi hota
> - Yeh "Guard" pattern hai

---

### 2.3 — Database Session Dependency

```python
# Saath mein `get_db` dependency bhi resolve hui
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    # SQLAlchemy async_sessionmaker se naya session create hua
    async with async_session() as session:
        # ✅ session = AsyncSession object (database connection pool se)
        yield session   # Route function ko diya
        # (route complete hone ke baad — session automatically close hoga)
```

> **Connection Pool:**
> - Actual PostgreSQL TCP connection already pool mein ready hai
> - `async_session()` ne pool se ek connection "borrow" kiya
> - Request complete hone par connection wapis pool mein

---

## ═══════════════════════════════════════════
## STEP 3 — Pydantic Validation: JSON Bytes → Python Object
### File: `app/schemas/meeting_note.py`
## ═══════════════════════════════════════════

### 3.1 — FastAPI ka Internal Deserialization

```
[Raw JSON string from request body]
    "{"raw_notes":"Met Rajesh...","meeting_date":"2026-08-10"}"
    ↓
FastAPI internally:
    raw_bytes = await request.body()
    json_dict = json.loads(raw_bytes)
    # json_dict = {
    #     "raw_notes": "Met Rajesh Sharma today. Interested in business loan.",
    #     "meeting_date": "2026-08-10"
    # }
    ↓
    request_obj = MeetingNoteProcessRequest(**json_dict)
    # Yahan Pydantic ka magic shuru hota hai
```

---

### 3.2 — Pydantic Model Field-by-Field Processing

```python
class MeetingNoteProcessRequest(BaseModel):

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # FIELD 1: raw_notes
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    raw_notes: str = Field(..., min_length=1)
    # INPUT: "Met Rajesh Sharma today. Interested in business loan."
    # Pydantic checks:
    #   [1] Type check: is it str? ✅ YES
    #   [2] min_length=1: len("Met Rajesh...") = 52 ≥ 1 ✅
    # ⚠️ Agar empty string "" aaya → ValidationError: min_length violated
    # ⚠️ Agar None aaya → ValidationError: str required

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # FIELD 2: meeting_date
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    meeting_date: date | None = None
    # INPUT: "2026-08-10" (string)
    # Pydantic ne AUTOMATICALLY string → Python date object convert kiya:
    #   date.fromisoformat("2026-08-10") → date(2026, 8, 10)
    # ⚠️ Agar "2026-13-45" aaya → ValidationError: invalid date
    # ✅ "2026-08-10" → date(2026, 8, 10)
    # (known_client_id field JSON mein nahi tha → default=None use hoga)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # FIELD 3: known_client_id
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    known_client_id: int | None = Field(default=None, gt=0)
    # INPUT: field missing from JSON → None (default)
    # ✅ None is allowed (int | None)
    # ⚠️ Agar 0 aaya → ValidationError: gt=0 violated (must be > 0)
    # ⚠️ Agar -5 aaya → ValidationError: gt=0 violated

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # FIELD 4: source_type
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    source_type: MeetingSourceType = Field(default=MeetingSourceType.PASTED_NOTE)
    # INPUT: field missing from JSON → default=MeetingSourceType.PASTED_NOTE
    # MeetingSourceType.PASTED_NOTE.value = "pasted_note"
```

---

### 3.3 — Custom `@field_validator` Chala

```python
@field_validator("raw_notes")
@classmethod
def validate_raw_notes(cls, value: str) -> str:
    # Yeh AUTOMATICALLY chala after basic type validation
    # value = "Met Rajesh Sharma today. Interested in business loan."
    
    settings = get_settings()
    # settings object LRU-cached hai — pehli baar env vars padhe, baad mein cache se

    stripped = value.strip()
    # stripped = "Met Rajesh Sharma today. Interested in business loan."
    # (already trimmed tha JS side se, lekin double safety)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # CHECK 1: Empty string?
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    if not stripped:
        # ⚠️ → FastAPI would return HTTP 422 Unprocessable Entity:
        # {"detail": [{"loc": ["body", "raw_notes"], "msg": "raw_notes cannot be empty."}]}
        raise ValueError("raw_notes cannot be empty.")
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # CHECK 2: Character limit
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # settings.raw_notes_max_chars typically = 10000
    if len(stripped) > settings.raw_notes_max_chars:
        # ⚠️ → HTTP 422 with char limit message
        raise ValueError(f"Cannot exceed {settings.raw_notes_max_chars} chars.")
    
    # ✅ Validation passed
    # IMPORTANT: yahan `stripped` return kiya — cleaned value!
    # Agar user ne leading/trailing spaces daale → Pydantic automatically remove kar dega
    return stripped
```

**Final `request` object:**

```python
request = MeetingNoteProcessRequest(
    raw_notes    = "Met Rajesh Sharma today. Interested in business loan.",
    meeting_date = date(2026, 8, 10),    # Python date object
    known_client_id = None,
    source_type  = MeetingSourceType.PASTED_NOTE
)
# Type: MeetingNoteProcessRequest (Pydantic BaseModel subclass)
# ✅ Yeh object wapis route function mein inject hua
```

---

## ═══════════════════════════════════════════
## STEP 4 — Route Function Execution → Service Call
### File: `app/api/v1/routes_meeting_notes.py`
## ═══════════════════════════════════════════

### 4.1 — Route Function Body

```python
@router.post("/process", response_model=MeetingNoteProcessResponse)
async def process_meeting_note(
    request: Annotated[MeetingNoteProcessRequest, Body(...)],
    db: AsyncSession = Depends(get_db),
) -> dict:
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Call chain: Route → Service
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    try:
        # MeetingProcessingService instantiated (per-request fresh object)
        # .process_notes() ko do cheezein di:
        #   1. db = AsyncSession (database connection)
        #   2. request = validated Pydantic object
        return await MeetingProcessingService().process_notes(db, request)
        
    except AIExtractionError as exc:
        # 🔴 AI service completely fail ho gayi (Groq + Gemini dono fail)
        # HTTP 502 Bad Gateway → Client ko bataya: upstream dependency fail
        raise HTTPException(status_code=502, detail=str(exc))
    
    # Baaki exceptions (SQLAlchemy errors, etc.) unhandled rahenge
    # → FastAPI ka default 500 Internal Server Error return karega
```

> **`response_model=MeetingNoteProcessResponse`** — Yeh decorator parameter FastAPI ko batata hai:
> - Route function jo bhi dict return kare, use `MeetingNoteProcessResponse` Pydantic model se validate karo
> - Sensitive fields automatically strip ho jayenge (agar koi extra field ho)
> - JSON serialization bhi Pydantic handle karegi

---

## ═══════════════════════════════════════════
## STEP 5 — First DB Write: Meeting Row Create (Partial Data)
### File: `app/services/meeting_processing_service.py`
## ═══════════════════════════════════════════

### 5.1 — Service Entry: Default Date + Meeting Object Creation

```python
async def process_notes(
    self,
    db: AsyncSession,
    request: MeetingNoteProcessRequest
) -> dict[str, Any]:

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Date resolution
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    meeting_date = request.meeting_date or date.today()
    # request.meeting_date = date(2026, 8, 10) → use kiya
    # Agar None hota → date.today() = date(2026, 8, 10) (aaj ki date)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # SQLAlchemy Meeting Object
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    meeting = Meeting(
        # ABHI NAHI PATA — AI processing ke baad pata chalega
        client_id = None,
        
        # IMMEDIATELY AVAILABLE DATA
        raw_notes    = request.raw_notes,          # "Met Rajesh Sharma..."
        meeting_date = meeting_date,               # date(2026, 8, 10)
        source_type  = request.source_type.value,  # "pasted_note" (string, not enum)
        
        # PLACEHOLDER VALUES — baad mein update honge
        summary                          = "",
        key_discussion_points_json       = "[]",   # Empty JSON array string
        concerns_json                    = "[]",
        
        # FAIL-SAFE STATUS — agar kuch bhi fail hua toh DB mein yeh status rahega
        # Koi data silently drop nahi hoga — manual review ke liye marked
        status                           = MeetingStatus.MANUAL_REVIEW_REQUIRED.value,
        
        # CLIENT IDENTIFICATION — abhi unknown
        client_identification_status     = "unknown",
        client_identification_confidence = 0.0,
    )
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # DB mein track karo (commit nahi)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    db.add(meeting)
    # SQLAlchemy session ne is object ko "pending" state mein add kiya
    # Abhi tak PostgreSQL ko kuch nahi gaya
    
    await db.flush()
    # FLUSH kya karta hai:
    #   1. Session ke pending objects ko SQL mein translate kiya
    #   2. PostgreSQL ko INSERT statement bheja:
    #      INSERT INTO meetings (client_id, raw_notes, meeting_date, ...)
    #      VALUES (NULL, 'Met Rajesh...', '2026-08-10', ...)
    #      RETURNING id;   ← PostgreSQL ne auto-generated id wapas diya
    #   3. meeting.id = 101  ← ab available hai
    #   4. TRANSACTION ABHI OPEN HAI — commit nahi hua
    #      Agar aage kuch fail hua → rollback ho sakta hai
```

> **`flush()` vs `commit()` ka fark:**
> | Action | `flush()` | `commit()` |
> |--------|-----------|------------|
> | SQL execute hoti hai | ✅ | ✅ |
> | Transaction ends | ❌ | ✅ |
> | Other sessions can see | ❌ | ✅ |
> | Rollback possible | ✅ | ❌ |
>
> **Kyun flush pehle?** — Hume `meeting.id` chahiye tha taaki AI audit log mein `meeting_id=101` save kar sakein.
> Agar pehle commit karte aur baad mein AI fail hoti, toh ek "zombie" meeting row rehti.

---

## ═══════════════════════════════════════════
## STEP 6 — AI Routing Service: Translation + Smart Fallback
### File: `app/services/ai_routing_service.py`
## ═══════════════════════════════════════════

### 6.1 — Service Instantiation + Entry

```python
# MeetingProcessingService ne yeh call kiya:
result = await AIRoutingService(settings).route_and_extract(
    raw_notes   = meeting.raw_notes,    # "Met Rajesh Sharma..."
    meeting_date = meeting_date,        # date(2026, 8, 10)
    meeting_id   = meeting.id           # 101 (flush ke baad available hua)
)
```

---

### 6.2 — Hinglish Pre-Processing (Economy/Translation Model)

```python
async def route_and_extract(self, raw_notes, meeting_date, meeting_id):

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PRE-PROCESSING: Hinglish → Clean English
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    try:
        # Economy provider = Groq (cheap + fast)
        trans_provider = get_ai_provider(self.settings.ai_economy_provider, self.settings)
        # ai_economy_provider = "groq"
        
        # asyncio.to_thread() kyon?
        # Provider ka .translate_transcript() ek SYNCHRONOUS function hai
        # (requests library use karta hai, jo blocking hai)
        # Directly await nahi kar sakte — event loop block ho jayega
        # to_thread() → OS thread pool mein bheja → event loop free raha
        clean_notes = await asyncio.to_thread(
            trans_provider.translate_transcript,
            raw_notes
            # Groq API ko yeh prompt gaya:
            # "Translate the following to clean English, preserving all business facts:
            #  Met Rajesh Sharma today. Interested in business loan."
        )
        # clean_notes = "Met Rajesh Sharma today. He expressed interest in a business loan."
        # (Pure English, koi Hinglish nahi)
        
    except Exception:
        # 🟡 Translation fail → Original notes use karo (non-critical)
        # Log mein record hoga, lekin processing continue rahegi
        clean_notes = raw_notes
```

---

### 6.3 — Primary AI Call: Groq (Economy Model)

```python
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ATTEMPT 1: Groq (Llama-3.3-70B)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    try:
        result = await self._call_and_validate(
            clean_notes,
            meeting_date,
            provider_name = "groq",                    # settings.ai_economy_provider
            model_name    = "llama-3.3-70b-versatile", # settings.ai_economy_model
            meeting_id    = 101
        )
        return result.payload   # ✅ Groq succeed → Gemini skip
        
    except (AIExtractionError, ValidationError):
        # ⚠️ Groq fail ya invalid JSON diya
        # Yahan silently pass karo → Gemini try karo
        pass
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ATTEMPT 2: Gemini (Review Model) — Fallback
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    result = await self._call_and_validate(
        clean_notes,
        meeting_date,
        provider_name = "gemini",          # settings.ai_review_provider
        model_name    = "gemini-2.5-flash", # settings.ai_review_model
        meeting_id    = 101
    )
    # ⚠️ Agar Gemini bhi fail → AIExtractionError raise → Step 4 mein 502 return hoga
    return result.payload
```

---

## ═══════════════════════════════════════════
## STEP 6A — `_call_and_validate()`: AI API HTTP Call + Schema Check + Audit Log
### File: `app/services/ai_routing_service.py`
## ═══════════════════════════════════════════

### 6A.1 — AI Provider Call (HTTP to External API)

```python
async def _call_and_validate(
    self, raw_notes, meeting_date, provider_name, model_name, meeting_id
):
    provider = get_ai_provider(provider_name, self.settings)
    # get_ai_provider() → GroqProvider instance (ya GeminiProvider)
    # Provider object mein API key stored hai (env var se)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Synchronous HTTP call → thread pool
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    result = await asyncio.to_thread(
        provider.extract_meeting_intelligence,
        raw_notes,
        meeting_date,
        model_name
    )
```

**Groq API ko jo actual HTTP request gaya:**

```http
POST https://api.groq.com/openai/v1/chat/completions HTTP/1.1
Authorization: Bearer gsk_xxxxxxxxxxxx
Content-Type: application/json

{
  "model": "llama-3.3-70b-versatile",
  "messages": [
    {
      "role": "system",
      "content": "You are a banking relationship manager assistant. Extract structured meeting intelligence from notes. Return ONLY valid JSON matching this schema: {client_identification: {...}, meeting_summary: string, key_discussion_points: [...], commitments: [...], concerns: [...], products_owned: [...]}"
    },
    {
      "role": "user", 
      "content": "Meeting Date: 2026-08-10\n\nNotes: Met Rajesh Sharma today. He expressed interest in a business loan."
    }
  ],
  "temperature": 0.1,
  "response_format": {"type": "json_object"}
}
```

**Groq ka Response:**

```json
{
  "choices": [{
    "message": {
      "content": "{\"client_identification\": {\"suggested_client_name\": \"Rajesh Sharma\", \"confidence\": 0.92, \"reasoning\": \"Full name mentioned directly\"}, \"meeting_summary\": \"Rajesh Sharma expressed interest in a business loan product.\", \"key_discussion_points\": [\"Business loan interest\"], \"commitments\": [{\"description\": \"Send documents by Friday\", \"due_date\": \"2026-08-14\", \"commitment_type\": \"action_item\", \"owner\": \"bank\"}], \"concerns\": [{\"description\": \"Processing time concern\", \"severity\": \"medium\"}], \"products_owned\": [\"Business Loan\"]}"
    }
  }],
  "usage": {
    "prompt_tokens": 245,
    "completion_tokens": 187,
    "total_tokens": 432
  },
  "model": "llama-3.3-70b-versatile"
}
```

---

### 6A.2 — Provider Internal Processing

```python
# GroqProvider.extract_meeting_intelligence() ke andar:

# 1. HTTP response mila
raw_content = response.choices[0].message.content
# raw_content = '{"client_identification": {...}, "meeting_summary": "...", ...}'

# 2. JSON parse kiya
payload_dict = json.loads(raw_content)

# 3. Timing calculate ki
latency_ms = (time.time() - start_time) * 1000   # e.g., 1240ms

# 4. Cost calculate ki
cost_usd = calculate_cost(
    provider="groq",
    model="llama-3.3-70b-versatile",
    input_tokens=245,
    output_tokens=187
)
# cost_usd ≈ 0.0021

# 5. AIResult namedtuple return kiya
return AIResult(
    payload = payload_dict,
    latency_ms = 1240,
    cost_usd = 0.0021,
    input_tokens = 245,
    output_tokens = 187
)
```

---

### 6A.3 — Pydantic Schema Validation (AI Output)

```python
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # AI response ko schema se validate karo
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # File: app/schemas/ai_extraction.py
    MeetingExtraction.model_validate(result.payload)
    # Yeh check karta hai:
    #   - client_identification field present hai? ✅
    #   - confidence 0.0-1.0 ke beech hai? ✅
    #   - commitments list of dicts hai? ✅
    #   - due_date valid date format hai? ✅
    # ⚠️ Agar AI ne garbled JSON diya → ValidationError → caller mein caught → fallback
```

---

### 6A.4 — Audit Log DB Save

```python
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Audit log: cost tracking + debugging
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    await self._log_audit(
        meeting_id   = 101,
        provider     = "groq",
        model        = "llama-3.3-70b-versatile",
        result       = result,
        success      = True
    )
    # PostgreSQL mein INSERT:
    # ai_extraction_logs table:
    # ┌────┬────────────┬──────────┬──────────────────────┬────────────┬──────────┬─────────────┐
    # │ id │ meeting_id │ provider │ model                │ latency_ms │ cost_usd │ success     │
    # ├────┼────────────┼──────────┼──────────────────────┼────────────┼──────────┼─────────────┤
    # │ 88 │ 101        │ groq     │ llama-3.3-70b-ver... │ 1240       │ 0.0021   │ true        │
    # └────┴────────────┴──────────┴──────────────────────┴────────────┴──────────┴─────────────┘
    
    return result   # AIResult object wapis caller ko
```

---

## ═══════════════════════════════════════════
## STEP 7 — Client Identification: Fuzzy Matching Algorithm
### File: `app/services/client_identification_service.py`
## ═══════════════════════════════════════════

### 7.1 — Extraction se Data Nikala

```python
# MeetingProcessingService ne yeh call kiya:
extraction = result  # AI ka processed dict
client_name = extraction["client_identification"]["suggested_client_name"]
# client_name = "Rajesh Sharma"

confidence = extraction["client_identification"]["confidence"]
# confidence = 0.92  (0.0 to 1.0)

client, id_status, warnings = await ClientIdentificationService(settings).resolve_client(
    db              = db,
    suggested_name  = "Rajesh Sharma",
    confidence      = 0.92,
    known_client_id = None    # User ne dropdown mein koi select nahi kiya tha
)
```

---

### 7.2 — `resolve_client()` Complete Logic

```python
async def resolve_client(self, db, suggested_name, confidence, known_client_id=None):

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PATH A: User ne manually select kiya tha?
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    if known_client_id:
        client = await db.get(Client, known_client_id)
        # SELECT * FROM clients WHERE id = ? (primary key lookup — O(1))
        if client:
            return client, "identified", []
        # ⚠️ Agar known_client_id exist nahi karta DB mein → None return
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PATH B: AI ke naam se match karo
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Step 1: Normalize
    normalized = normalize_text("Rajesh Sharma")
    # normalize_text() kya karta hai:
    #   lower() → "rajesh sharma"
    #   strip() → "rajesh sharma"
    #   multiple spaces → single space
    #   special chars remove (optional)
    # normalized = "rajesh sharma"
    
    # Step 2: ALL clients DB se load karo
    clients = list((await db.scalars(select(Client))).all())
    # SELECT * FROM clients;
    # ⚠️ Scaling concern: 1000+ clients hone par yeh slow ho sakta hai
    # Current version mein acceptable (banking RM ka typical client count)
    
    # Step 3: Exact match
    exact = [c for c in clients if c.normalized_name == "rajesh sharma"]
    # ✅ Rajesh already DB mein hai: exact = [<Client id=7, name="Rajesh Sharma">]
    
    # Confidence threshold check
    # settings.client_auto_match_threshold typically = 0.85
    if exact and confidence >= 0.85:
        # 0.92 >= 0.85 ✅ Auto-match
        return exact[0], "identified", []
        # exact[0] = Client(id=7, name="Rajesh Sharma")
        # "identified" = status string
        # [] = no warnings
    
    # Step 4: Fuzzy match (agar exact match nahi mila)
    # (Rajesh ka exact match mila, toh yeh section skip)
    close_matches = [
        c for c in clients
        if similarity(c.normalized_name, "rajesh sharma") >= 0.85
    ]
    # similarity() → typically Levenshtein distance ya SequenceMatcher ratio
    # "rajesh sharma" vs "rajesh sharma" → 1.0 (perfect)
    # "rajesh sharma" vs "rajesh sharme" → ~0.93 (close enough)
    # "rajesh sharma" vs "rakesh sharma" → ~0.87 (still close)
    # "rajesh sharma" vs "raj kumar" → ~0.45 (too different)
    
    if len(close_matches) == 1 and confidence >= 0.85:
        return close_matches[0], "identified", []
    
    # Multiple matches OR low confidence → User confirmation required
    return None, "client_identification_required", ["New client; confirmation required."]
```

**Return values is case mein:**

```python
client    = Client(id=7, name="Rajesh Sharma", normalized_name="rajesh sharma")
id_status = "identified"
warnings  = []
```

---

## ═══════════════════════════════════════════
## STEP 8 — Multi-Table DB Update: Meeting + Commitments + Memory + Rules
### File: `app/services/meeting_processing_service.py`
## ═══════════════════════════════════════════

### 8.1 — Meeting Row Update (Placeholder → Real Data)

```python
# NIKLA: extraction dict (AI ka complete output)
# GIRA: Meeting row jo Step 5 mein create hua tha (id=101)

# meeting object ab update ho raha hai (same SQLAlchemy object, memory mein)
meeting.client_id   = client.id          # None → 7
meeting.summary     = extraction.get("meeting_summary")
# "Rajesh Sharma expressed interest in a business loan product."

meeting.key_discussion_points_json = json.dumps(
    extraction.get("key_discussion_points")
)
# '["Business loan interest"]'

meeting.concerns_json = json.dumps(extraction.get("concerns"))
# '[{"description": "Processing time concern", "severity": "medium"}]'

meeting.status = "processed"
# MANUAL_REVIEW_REQUIRED → processed (✅ happy path)

meeting.client_identification_status     = "identified"   # unknown → identified
meeting.client_identification_confidence = 0.92           # 0.0 → 0.92

db.add(meeting)
# SQLAlchemy ne dirty tracking se pata lagaya kaunse fields change hue
# UPDATE statement ready ho gaya (abhi execute nahi hua — flush/commit pe hoga)
```

---

### 8.2 — Client Products Merge

```python
if client:
    self._merge_client_products(client, extraction.get("products_owned") or [])
    # extraction["products_owned"] = ["Business Loan"]
    
    # _merge_client_products ke andar:
    existing = json.loads(client.products_owned_json or "[]")
    # existing = []  (pehli baar)
    
    new_products = list(set(existing + ["Business Loan"]))
    # new_products = ["Business Loan"]
    
    client.products_owned_json = json.dumps(new_products)
    # client.products_owned_json = '["Business Loan"]'
    # Client table mein update hoga commit par
```

---

### 8.3 — `CommitmentService.upsert_commitments()` Deep Dive

```python
created, updated = await self.commitments.upsert_commitments(
    db,
    client_id              = 7,
    meeting_id             = 101,
    extracted_commitments  = [
        {
            "description":       "Send documents by Friday",
            "due_date":          "2026-08-14",
            "commitment_type":   "action_item",
            "owner":             "bank"
        }
    ]
)
```

**`upsert_commitments()` ke andar:**

```python
async def upsert_commitments(self, db, client_id, meeting_id, extracted_commitments):
    created = []
    updated = []
    
    for comm_data in extracted_commitments:
        # "Send documents by Friday"
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # DUPLICATE CHECK: kya similar commitment already open hai?
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        existing = await db.execute(
            select(Commitment).where(
                Commitment.client_id == 7,
                Commitment.status == "open",
                # Fuzzy check ya exact match on description
                Commitment.description.ilike("%Send documents%")
            )
        )
        existing_comm = existing.scalar_one_or_none()
        
        if existing_comm:
            # UPSERT: existing commitment update karo
            existing_comm.due_date = date.fromisoformat("2026-08-14")
            existing_comm.meeting_id = 101  # Latest meeting se link
            updated.append(existing_comm)
        else:
            # CREATE: naya commitment
            new_comm = Commitment(
                client_id       = 7,
                meeting_id      = 101,
                description     = "Send documents by Friday",
                due_date        = date(2026, 8, 14),
                commitment_type = "action_item",
                owner           = "bank",
                status          = "open"
            )
            db.add(new_comm)
            await db.flush()  # ← commitment.id = 55 chahiye tha
            
            # CommitmentMeetingLink: many-to-many table
            link = CommitmentMeetingLink(
                commitment_id = 55,
                meeting_id    = 101
            )
            db.add(link)
            created.append(new_comm)
    
    return created, updated
    # created = [Commitment(id=55, description="Send documents by Friday")]
    # updated = []
```

**Tables touched:**

```
commitments table:
┌────┬───────────┬────────────┬──────────────────────────────┬────────────┬────────┐
│ id │ client_id │ meeting_id │ description                  │ due_date   │ status │
├────┼───────────┼────────────┼──────────────────────────────┼────────────┼────────┤
│ 55 │ 7         │ 101        │ Send documents by Friday     │ 2026-08-14 │ open   │
└────┴───────────┴────────────┴──────────────────────────────┴────────────┴────────┘

commitment_meeting_links table:
┌─────────────────┬────────────┐
│ commitment_id   │ meeting_id │
├─────────────────┼────────────┤
│ 55              │ 101        │
└─────────────────┴────────────┘
```

---

### 8.4 — `MemoryService.update_client_memory()` Deep Dive

```python
await self.memory.update_client_memory(db, client_id=7)
```

**Memory service ke andar:**

```python
async def update_client_memory(self, db, client_id):
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Pichli N meetings padho (rolling window)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    recent_meetings = await db.execute(
        select(Meeting)
        .where(Meeting.client_id == 7)
        .order_by(Meeting.meeting_date.desc())
        .limit(5)   # settings.memory_rolling_window = 5
    )
    meetings = recent_meetings.scalars().all()
    # meetings = [Meeting(id=101, summary="Rajesh discussed business loan"), ...]
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Pending commitments padho
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    pending_comms = await db.execute(
        select(Commitment)
        .where(
            Commitment.client_id == 7,
            Commitment.status == "open"
        )
    )
    open_commitments = pending_comms.scalars().all()
    # open_commitments = [Commitment(id=55, description="Send documents by Friday")]
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Rolling summary generate karo
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # (Template-based ya lightweight AI call)
    summary_parts = []
    
    for m in meetings:
        summary_parts.append(f"[{m.meeting_date}] {m.summary}")
    
    commitment_text = ", ".join([
        f"{c.description} (due: {c.due_date})"
        for c in open_commitments
    ])
    
    rolling_summary = "\n".join(summary_parts)
    if commitment_text:
        rolling_summary += f"\n\nOpen commitments: {commitment_text}"
    
    # client object update karo
    client = await db.get(Client, 7)
    client.rolling_summary = rolling_summary
    # "Rajesh discussed a business loan.\nOpen commitments: Send documents by Friday (due: 2026-08-14)"
    
    db.add(client)
    # ✅ Client row update queued (commit par execute hoga)
```

---

### 8.5 — `RulesEngineService.sync_client_tasks_and_risks()`

```python
await RulesEngineService.sync_client_tasks_and_risks(db, client_id=7)
```

**Rules engine ke andar:**

```python
@staticmethod
async def sync_client_tasks_and_risks(db, client_id):

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # RULE 1: Open commitments → FollowUpTask rows
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    open_commitments = [...]  # client 7 ke open commitments
    
    for commitment in open_commitments:
        # Kya task already exist karta hai?
        existing_task = await db.execute(
            select(FollowUpTask)
            .where(FollowUpTask.commitment_id == commitment.id)
        )
        task = existing_task.scalar_one_or_none()
        
        is_overdue = commitment.due_date < date.today()
        # date(2026, 8, 14) < date(2026, 8, 10) → False (still upcoming)
        
        if not task:
            new_task = FollowUpTask(
                client_id     = 7,
                commitment_id = 55,
                is_overdue    = False,
                priority      = "medium"
            )
            db.add(new_task)
        else:
            # Overdue status update karo
            task.is_overdue = is_overdue
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # RULE 2: High severity concerns → RiskSignal rows
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # concerns_json = '[{"description": "Processing time concern", "severity": "medium"}]'
    concerns = json.loads(meeting.concerns_json)
    
    for concern in concerns:
        if concern["severity"] == "high":
            # Naya RiskSignal row
            risk = RiskSignal(
                client_id   = 7,
                meeting_id  = 101,
                description = concern["description"],
                severity    = "high"
            )
            db.add(risk)
    # "medium" severity → RiskSignal nahi bana is case mein
```

---

### 8.6 — `db.commit()` — Sab Kuch Permanently Save

```python
await db.commit()
```

**Is ek commit() mein kya kya execute hua (PostgreSQL ke andar):**

```sql
BEGIN;  ← pehle se open tha (Step 5 se)

-- Meeting row update (partial → full data)
UPDATE meetings SET
    client_id = 7,
    summary = 'Rajesh Sharma expressed interest in a business loan product.',
    key_discussion_points_json = '["Business loan interest"]',
    concerns_json = '[{"description": "Processing time concern", "severity": "medium"}]',
    status = 'processed',
    client_identification_status = 'identified',
    client_identification_confidence = 0.92
WHERE id = 101;

-- Client products update
UPDATE clients SET
    products_owned_json = '["Business Loan"]',
    rolling_summary = 'Rajesh discussed a business loan.\nOpen commitments: ...'
WHERE id = 7;

-- New commitment
INSERT INTO commitments (client_id, meeting_id, description, due_date, commitment_type, owner, status)
VALUES (7, 101, 'Send documents by Friday', '2026-08-14', 'action_item', 'bank', 'open')
RETURNING id;  → 55

-- Commitment-Meeting link
INSERT INTO commitment_meeting_links (commitment_id, meeting_id)
VALUES (55, 101);

-- FollowUp task
INSERT INTO follow_up_tasks (client_id, commitment_id, is_overdue, priority)
VALUES (7, 55, false, 'medium');

-- AI audit log (from Step 6A)
INSERT INTO ai_extraction_logs (meeting_id, provider, model, latency_ms, cost_usd, success)
VALUES (101, 'groq', 'llama-3.3-70b-versatile', 1240, 0.0021, true);

COMMIT;  ← Sab permanently save! Rollback possible nahi ab.
```

> **ACID Guarantee:**
> - **A**tomic: Ya sab save hoga, ya kuch nahi (ek bhi fail → sab rollback)
> - **C**onsistent: Foreign keys valid rahenge (client_id=7 exist karta hai)
> - **I**solated: Doosre requests ka is transaction pe koi effect nahi
> - **D**urable: Commit ke baad power cut bhi aaye toh data safe

---

## ═══════════════════════════════════════════
## STEP 9 — Redis Queue: Background Job Enqueue
### File: `app/services/meeting_processing_service.py`
## ═══════════════════════════════════════════

### 9.1 — ARQ Pool se Job Enqueue

```python
pool = get_arq_pool()
# ARQ pool = Redis connection pool (already initialized at app startup)
# Redis server locally chal raha hai ya managed service (e.g., Redis Cloud)

if client and pool:
    await pool.enqueue_job(
        "generate_meeting_embeddings",     # Worker function naam
        meeting.id,                        # Positional arg: 101
        organization_id = "default",
        user_id         = "default",
        _job_id         = f"generate_meeting_embeddings_101"
        # _job_id: idempotency key
        # Agar same job already queue mein hai → duplicate nahi banega
        # Network retry safe hai
    )
```

**Redis ke andar kya pada:**

```
Redis key: "arq:job:generate_meeting_embeddings_101"
Redis value (serialized):
{
    "function": "generate_meeting_embeddings",
    "args": [101],
    "kwargs": {"organization_id": "default", "user_id": "default"},
    "enqueue_time": 1723311000.123,
    "job_id": "generate_meeting_embeddings_101"
}
TTL: 24 hours (job expire hoga agar worker na uthaye)
```

> **Kyun background queue?**
> - Embedding generation CPU + memory intensive hai (~500ms-2s)
> - User ko response dene mein delay nahi honi chahiye
> - Main API request 200ms ke andar respond kare (embedding ke bina)
> - Worker alag process mein chalega — API server free rahega

---

## ═══════════════════════════════════════════
## STEP 9A — ARQ Worker: Embedding Generation (Parallel Process)
### File: `app/jobs/embedding_jobs.py`
## ═══════════════════════════════════════════

### 9A.1 — Worker Process Structure

```
[SEPARATE OS PROCESS — API server se alag]
ARQ Worker process:
    └── Redis poll kar raha tha (every 0.1s by default)
    └── "generate_meeting_embeddings_101" job mila
    └── generate_meeting_embeddings() function call kiya
```

---

### 9A.2 — Embedding Job Execution

```python
async def generate_meeting_embeddings(
    ctx: dict,
    meeting_id: int,           # 101
    organization_id: str,      # "default"
    user_id: str               # "default"
):
    async with SessionLocal() as db:
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # Step 1: DB se meeting fetch karo
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        result = await db.execute(
            select(Meeting).where(Meeting.id == 101)
        )
        meeting = result.scalar_one()
        # SELECT * FROM meetings WHERE id = 101;
        # meeting.raw_notes = "Met Rajesh Sharma today. Interested in business loan."
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # Step 2: Text → Chunks → Vectors
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # CPU-intensive: Thread pool mein bheja
        chunks = await asyncio.to_thread(
            generate_embeddings_for_text,
            meeting.raw_notes
        )
        # generate_embeddings_for_text ke andar:
        #   1. Text ko sentences mein toda (NLTK ya simple split)
        #   2. sentence-transformers model load kiya (all-MiniLM-L6-v2 ya similar)
        #   3. model.encode([sentence1, sentence2]) → numpy arrays
        #   4. 384-dimensional vectors (float32)
        
        # chunks = [
        #   {
        #     "chunk_index": 0,
        #     "chunk_text": "Met Rajesh Sharma today.",
        #     "embedding": [0.23, -0.11, 0.45, ..., 0.08]  # 384 floats
        #   },
        #   {
        #     "chunk_index": 1,
        #     "chunk_text": "Interested in business loan.",
        #     "embedding": [0.31, 0.02, -0.19, ..., 0.14]  # 384 floats
        #   }
        # ]
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # Step 3: Purane embeddings delete (idempotency)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        await db.execute(
            delete(MeetingEvidence).where(MeetingEvidence.meeting_id == 101)
        )
        # Agar job retry hua (Redis crash ke baad) → duplicate embeddings nahi banenge
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # Step 4: pgvector table mein save
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        for chunk in chunks:
            evidence = MeetingEvidence(
                meeting_id  = 101,
                chunk_index = chunk["chunk_index"],
                chunk_text  = chunk["chunk_text"],
                embedding   = chunk["embedding"]   # pgvector: vector(384) column type
            )
            db.add(evidence)
        
        await db.commit()
        # INSERT INTO meeting_evidence (meeting_id, chunk_index, chunk_text, embedding)
        # VALUES (101, 0, 'Met Rajesh...', '[0.23, -0.11, ...]'),
        #        (101, 1, 'Interested in...', '[0.31, 0.02, ...]');
```

**meeting_evidence table (pgvector):**

```
┌────┬────────────┬─────────────┬───────────────────────────────┬──────────────────────┐
│ id │ meeting_id │ chunk_index │ chunk_text                    │ embedding (vector384)│
├────┼────────────┼─────────────┼───────────────────────────────┼──────────────────────┤
│ 201│ 101        │ 0           │ Met Rajesh Sharma today.      │ [0.23, -0.11, ...]   │
│ 202│ 101        │ 1           │ Interested in business loan.  │ [0.31, 0.02, ...]    │
└────┴────────────┴─────────────┴───────────────────────────────┴──────────────────────┘
```

> **Yeh embeddings kyun chahiye?**
> "Ask Client" feature ke liye — user puchega "Rajesh ne pichli baar kya bola tha?"
> System cosine similarity search karega: query vector vs stored embeddings
> pgvector ka `<=>` operator: `ORDER BY embedding <=> $query_vector LIMIT 5`

---

## ═══════════════════════════════════════════
## STEP 10 — Response Construction + Pydantic Serialization
### File: `app/schemas/meeting_note.py`
## ═══════════════════════════════════════════

### 10.1 — Service Return Dict

```python
# MeetingProcessingService._process_extracted_meeting() ne return kiya:
return {
    "meeting_id":                    101,
    "client_status":                 "identified",
    "client_id":                     7,
    "requires_client_confirmation":  False,
    "meeting_summary":               "Rajesh Sharma expressed interest in a business loan product.",
    "meeting":                       meeting,        # SQLAlchemy Meeting object
    "extraction":                    extraction,     # AI dict
    "commitments_created":           created,        # [Commitment(id=55)]
    "commitments_updated":           updated,        # []
    "pending_commitments":           all_open,       # [Commitment(id=55)]
    "warnings":                      []
}
```

---

### 10.2 — FastAPI ka Response Serialization

```python
# Route decorator ne yeh specify kiya tha:
@router.post("/process", response_model=MeetingNoteProcessResponse)

# FastAPI ne service ka return dict liya
# MeetingNoteProcessResponse.model_validate(return_dict) call kiya
# Har field validate + serialize hua:

class MeetingNoteProcessResponse(BaseModel):
    meeting_id:                    int         # 101 ✅
    client_status:                 str         # "identified" ✅
    client_id:                     int | None  # 7 ✅
    requires_client_confirmation:  bool        # False ✅
    meeting_summary:               str         # "Rajesh discussed..." ✅
    meeting:                       MeetingRead # SQLAlchemy obj → Pydantic model
    extraction:                    MeetingExtractionRead
    commitments_created:           list[CommitmentRead]  # [CommitmentRead(id=55)]
    commitments_updated:           list[CommitmentRead]  # []
    pending_commitments:           list[CommitmentRead]
    warnings:                      list[str]   # []
    
    model_config = ConfigDict(from_attributes=True)
    # yeh setting SQLAlchemy objects ko directly accept karne deta hai
```

**Wire par gaya HTTP Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 842

{
  "meeting_id": 101,
  "client_status": "identified",
  "client_id": 7,
  "requires_client_confirmation": false,
  "meeting_summary": "Rajesh Sharma expressed interest in a business loan product.",
  "meeting": {
    "id": 101,
    "meeting_date": "2026-08-10",
    "status": "processed",
    "summary": "Rajesh Sharma expressed interest in a business loan product.",
    "raw_notes": "Met Rajesh Sharma today. Interested in business loan."
  },
  "extraction": { ... },
  "commitments_created": [
    {
      "id": 55,
      "description": "Send documents by Friday",
      "due_date": "2026-08-14",
      "status": "open"
    }
  ],
  "commitments_updated": [],
  "pending_commitments": [{ "id": 55, ... }],
  "warnings": []
}
```

---

## ═══════════════════════════════════════════
## STEP 11 — Browser: Response Receive → DOM Update → UI Refresh
### File: `app/web/app.js`
## ═══════════════════════════════════════════

### 11.1 — `await api()` Resume — payload Object Mila

```javascript
// Step 1 mein yahan await tha:
const payload = await api("/api/v1/meeting-notes/process", {...})
// JavaScript event loop ne resume kiya jab HTTP response aaya
// response.json() ne JSON string parse karke JavaScript object banaya:

// payload = {
//   meeting_id: 101,
//   client_status: "identified",
//   client_id: 7,
//   requires_client_confirmation: false,
//   meeting_summary: "Rajesh Sharma expressed interest in a business loan product.",
//   meeting: { id: 101, ... },
//   commitments_created: [{ id: 55, description: "Send documents by Friday", ... }],
//   commitments_updated: [],
//   pending_commitments: [{ id: 55, ... }],
//   warnings: []
// }
```

---

### 11.2 — `renderProcessResult(payload)` — DOM Update

```javascript
function renderProcessResult(payload) {
    
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // Main result panel update
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    els.processResult.innerHTML = `
        <div class="result-summary">
          <span class="status-pill done">
            ${escapeHtml(payload.client_status)}
          </span>
          <!-- "identified" dikhaya -->
          
          <strong>
            ${escapeHtml(payload.meeting_summary)}
          </strong>
          <!-- "Rajesh Sharma expressed interest in a business loan product." -->
          
          <span>Created: ${payload.commitments_created.length}</span>
          <!-- "Created: 1" -->
        </div>
    `
    // escapeHtml() kyon?: XSS prevention
    // Agar AI ne malicious HTML return kiya toh DOM injection nahi hoga
    
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // Client confirmation popup check
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    if (payload.requires_client_confirmation) {
        // New client — user ko confirm karna hoga
        state.pendingConfirmationMeetingId = payload.meeting_id
        els.confirmPanel.classList.remove("hidden")  // Popup dikhaya
    } else {
        // ✅ Client identified — directly set karo
        state.selectedClientId = payload.client_id   // state.selectedClientId = 7
        // state = global app state object
    }
}
```

---

### 11.3 — `refreshAll()` — Dashboard Data Reload

```javascript
async function refreshAll() {
    // Parallel mein teen API calls:
    await Promise.all([
        loadClients(),       // GET /api/v1/clients
        loadCommitments(),   // GET /api/v1/commitments
        loadPriorities()     // GET /api/v1/dashboard/priorities
    ])
}

// loadClients():
//   → GET /api/v1/clients → [{id:7, name:"Rajesh Sharma"}, ...]
//   → els.clientCount.textContent = "12 Clients"

// loadCommitments():
//   → GET /api/v1/commitments?status=open → [{id:55, description:"Send documents..."}, ...]
//   → els.pendingCount.textContent = "3 Pending"

// loadPriorities():
//   → GET /api/v1/dashboard/priorities
//   → Priorities list update → FollowUpTask rows dikhaye
```

---

### 11.4 — `loadMemory()` — Client Memory Panel

```javascript
if (payload.client_id) {
    await loadMemory(payload.client_id)  // loadMemory(7)
}

// loadMemory(7):
//   → GET /api/v1/clients/7/memory
//   → Response: {rolling_summary: "Rajesh discussed a business loan.\nOpen commitments: ..."}
//   → els.memoryPanel.textContent = rolling_summary
//   → Rajesh ki latest memory ab screen par dikhti hai

showToast("Meeting notes processed.")
// ✅ Green toast notification bottom-right corner mein 3 seconds ke liye
```

---

## ═══════════════════════════════════════════════════════════
## 🏁 COMPLETE END-TO-END DATA TRANSFORMATION CHAIN
## ═══════════════════════════════════════════════════════════

```
[RAW INPUT]
HTML <textarea> value:
"  Met Rajesh Sharma today. Interested in business loan.  "
        ↓ .trim()
JavaScript string: "Met Rajesh Sharma today. Interested in business loan."
        ↓ JSON.stringify()
HTTP body bytes: {"raw_notes":"Met Rajesh...","meeting_date":"2026-08-10"}
        ↓ TCP/IP Network
FastAPI receives raw bytes
        ↓ json.loads()
Python dict: {"raw_notes": "Met Rajesh...", "meeting_date": "2026-08-10"}
        ↓ Pydantic MeetingNoteProcessRequest(**dict)
        ↓ field_validator("raw_notes") → stripped & validated
Python object: MeetingNoteProcessRequest(raw_notes="Met Rajesh...", meeting_date=date(2026,8,10))
        ↓ MeetingProcessingService().process_notes()
SQLAlchemy Meeting(raw_notes="...", status="manual_review_required")
        ↓ db.flush() → PostgreSQL INSERT → id=101
Meeting.id = 101 available
        ↓ AIRoutingService().route_and_extract()
        ↓ asyncio.to_thread(translate_transcript) → Groq HTTP call
clean_notes = "Met Rajesh Sharma today. He expressed interest in a business loan."
        ↓ asyncio.to_thread(extract_meeting_intelligence, groq, llama-3.3-70b)
        ↓ Groq API HTTP call (external network)
        ↓ json.loads(response.choices[0].message.content)
extraction dict: {client_name:"Rajesh Sharma", confidence:0.92, summary:"...", commitments:[...]}
        ↓ MeetingExtraction.model_validate() → schema check
        ↓ _log_audit() → ai_extraction_logs INSERT
        ↓ ClientIdentificationService.resolve_client()
        ↓ SELECT * FROM clients + normalize_text + similarity()
client = Client(id=7, name="Rajesh Sharma"), id_status="identified"
        ↓ meeting.client_id = 7, meeting.status = "processed" (in-memory update)
        ↓ CommitmentService.upsert_commitments()
Commitment(id=55, description="Send documents by Friday") created
CommitmentMeetingLink(commitment_id=55, meeting_id=101) created
        ↓ MemoryService.update_client_memory()
client.rolling_summary = "Rajesh discussed business loan. Open: Send docs (2026-08-14)"
        ↓ RulesEngineService.sync()
FollowUpTask(commitment_id=55, is_overdue=False) created
        ↓ db.commit() ← ATOMIC: 6 tables mein changes permanently saved
        ↓ pool.enqueue_job("generate_meeting_embeddings", 101)
Redis key "arq:job:generate_meeting_embeddings_101" created
        ↓ Service returns dict
        ↓ FastAPI: MeetingNoteProcessResponse.model_validate()
        ↓ JSON serialization
HTTP 200 Response (JSON): {meeting_id:101, client_status:"identified", ...}
        ↓ TCP/IP Network
Browser receives bytes
        ↓ response.json() → JavaScript object
payload = {meeting_id:101, client_status:"identified", commitments_created:[...]}
        ↓ renderProcessResult(payload) → innerHTML update
        ↓ refreshAll() → 3 parallel GET requests → DOM updates
        ↓ loadMemory(7) → GET request → memory panel update
        ↓ showToast("Meeting notes processed.")
[FINAL OUTPUT]
✅ Screen updated, all panels refreshed, green toast visible

[BACKGROUND - PARALLEL]
ARQ Worker picks up Redis job
        ↓ SELECT Meeting WHERE id=101
        ↓ asyncio.to_thread(generate_embeddings_for_text)
        ↓ sentence-transformer model: text → 384-dim vectors
        ↓ DELETE old MeetingEvidence WHERE meeting_id=101
        ↓ INSERT MeetingEvidence x2 rows (pgvector columns)
        ↓ db.commit()
✅ RAG search ab possible for this meeting
```

---

## 📊 TABLES TOUCHED — Summary

| Table | Operation | When | Rows Affected |
|-------|-----------|------|---------------|
| `meetings` | INSERT | Step 5 (flush) | 1 new row (id=101) |
| `meetings` | UPDATE | Step 8 (commit) | id=101 updated |
| `clients` | UPDATE | Step 8 (commit) | id=7 products + rolling_summary |
| `commitments` | INSERT | Step 8.3 (flush) | id=55 |
| `commitment_meeting_links` | INSERT | Step 8.3 | (55, 101) |
| `follow_up_tasks` | INSERT | Step 8.5 | 1 new task |
| `ai_extraction_logs` | INSERT | Step 6A | provider audit row |
| `meeting_evidence` (pgvector) | DELETE + INSERT | Step 9A (background) | 2 embedding rows |

## 🌐 EXTERNAL HTTP CALLS — Summary

| Call | To | When | Blocking? | Fallback |
|------|----|------|-----------|---------|
| Translation | Groq API | Step 6.2 | No (thread) | Use original text |
| Extraction | Groq (Llama-3.3-70B) | Step 6.3 | No (thread) | Try Gemini |
| Extraction | Gemini 2.5-Flash | Step 6.3 | No (thread) | Raise 502 |
| Embeddings | (local model, no HTTP) | Step 9A | Thread pool | Job retry |

## ⏱️ TIMING BREAKDOWN (Typical)

```
Step 1  (Browser → HTTP)                  ~5ms
Step 2  (FastAPI routing + auth)          ~2ms
Step 3  (Pydantic validation)             ~1ms
Step 4  (Route function setup)            ~0.1ms
Step 5  (DB INSERT + flush)               ~10ms
Step 6  (Translation via Groq)            ~400ms
Step 6  (Extraction via Groq)             ~1200ms
Step 6A (Pydantic validate + audit log)   ~15ms
Step 7  (Client fuzzy match)              ~20ms  (SELECT all clients + similarity)
Step 8  (DB updates + commit)             ~30ms
Step 9  (Redis enqueue)                   ~5ms
Step 10 (Response serialization)          ~2ms
Step 11 (Browser render + refresh)        ~150ms

TOTAL API Response Time: ~1850ms (dominated by Groq call)
Background embedding: ~500ms (user ko nahi dikhta)
```
