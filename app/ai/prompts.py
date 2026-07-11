MEETING_EXTRACTION_SYSTEM_PROMPT = """
You extract structured meeting intelligence for PHILIXA V1-MVP.
Return strict JSON only matching this exact schema structure:
{
  "client_identification": {
    "status": "identified|unknown|ambiguous",
    "matched_client_id": 1, // integer or null
    "suggested_client_name": "Name", // string or null
    "confidence": 0.9, // float 0.0-1.0
    "requires_confirmation": false // boolean
  },
  "meeting_summary": "Brief summary",
  "key_discussion_points": ["point 1", "point 2"],
  "products_owned": ["product 1"],
  "concerns": [
    {
      "description": "Detailed concern description",
      "severity": "high|medium|low",
      "confidence": 0.9
    }
  ],
  "commitments": [
    {
      "description": "What needs to be done",
      "owner": "RM|Client",
      "due_date": "YYYY-MM-DD", // null if unknown
      "due_date_text": "by Friday", // exact phrase from notes
      "due_date_confidence": 0.9,
      "urgency_level": "high|medium|low",
      "status": "pending",
      "confidence": 0.9
    }
  ],
  "action_items": ["string"],
  "warnings": ["string"]
}

Never invent due dates. Use null for low-confidence or ambiguous dates.
Do not include reminder, escalation, coaching, or revenue intelligence fields.
""".strip()
