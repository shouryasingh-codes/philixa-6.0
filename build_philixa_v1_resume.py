from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether

out = Path('output/resume/Shourya_Singh_Resume_Philixa_Beta_Final_2026.pdf')
out.parent.mkdir(parents=True, exist_ok=True)
blue, ink, muted = HexColor('#1769E0'), HexColor('#172033'), HexColor('#415168')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle('RName', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=20, leading=22, textColor=ink, spaceAfter=0))
styles.add(ParagraphStyle('RContact', parent=styles['Normal'], fontName='Helvetica', fontSize=8.6, leading=11, textColor=muted, spaceAfter=5))
styles.add(ParagraphStyle('RSection', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.2, leading=12, textColor=blue, spaceBefore=4, spaceAfter=1))
styles.add(ParagraphStyle('RBody', parent=styles['Normal'], fontName='Helvetica', fontSize=8.7, leading=10.4, textColor=muted, spaceAfter=1))
styles.add(ParagraphStyle('RProject', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=11.3, textColor=ink, spaceAfter=0))
styles.add(ParagraphStyle('RStack', parent=styles['Normal'], fontName='Helvetica', fontSize=7.8, leading=9.3, textColor=muted, spaceAfter=0))
styles.add(ParagraphStyle('RBullet', parent=styles['Normal'], fontName='Helvetica', fontSize=8.65, leading=10.15, textColor=muted, leftIndent=9, firstLineIndent=-7, spaceAfter=0.5))
styles.add(ParagraphStyle('RSkill', parent=styles['Normal'], fontName='Helvetica', fontSize=8.45, leading=10.0, textColor=muted, spaceAfter=0))

def P(s, st): return Paragraph(s, styles[st])
def section(s): return P(s, 'RSection')
def project(s): return P('<b>'+s+'</b>', 'RProject')
def stack(s): return P(s, 'RStack')
def links(s): return P('<font color="#1769E0">'+s+'</font>', 'RStack')
def bullet(s): return P('• ' + s, 'RBullet')

story = [
    P('SHOURYA SINGH', 'RName'),
    P('+91 9610621152  |  shouryasingh3937@gmail.com  |  Jaipur, India  |  Open to Gurugram / Remote  |  <font color="#1769E0"><a href="https://www.linkedin.com/in/shourya-singh-954150392/"><u>LinkedIn</u></a></font>  |  <font color="#1769E0"><a href="https://github.com/shouryasingh-codes?tab=repositories"><u>GitHub</u></a></font>', 'RContact'),
    section('PROFESSIONAL SUMMARY'),
    P('Applied AI and backend developer building end-to-end LLM workflows, evidence-backed retrieval, voice-enabled copilots, and asynchronous Python services. Focused on reliable AI product features with validation, human review, and deployment-ready architecture.', 'RBody'),
    section('PROJECTS'),
    KeepTogether([
        project('PHILIXA - AI Meeting Intelligence Beta for Financial Advisors | 2026'),
        stack('FastAPI, PostgreSQL, pgvector, Redis, ARQ, Pydantic v2, faster-whisper, Deepgram, Sarvam TTS, Sentence Transformers, WhatsApp Cloud API, Docker, MinIO, WebSocket'),
        links('<a href="https://philixa-6-0.onrender.com"><u>Live Demo</u></a>  |  <a href="https://github.com/shouryasingh-codes/philixa-6.0"><u>GitHub</u></a>'),
        bullet('Built PHILIXA Beta, a multi-modal, reliability-first AI client-intelligence system for financial advisors that converts meetings into validated client memory, actionable follow-ups, voice-assisted workflows, and context-aware WhatsApp pre-meeting briefings.'),
        bullet('Built four meeting-input modes - paste notes, audio upload, live browser recording, and fast dictation - with dedicated solo and speaker-labeled meeting modes plus client auto-identification.'),
        bullet('Implemented a cost-aware two-stage AI pipeline: an economy SLM handles initial meeting extraction, while ambiguous, invalid, or high-risk outputs escalate to a stronger LLM; added Pydantic validation, manual-review fallback, and latency/cost audit logs.'),
        bullet('Built evidence-backed client memory using pgvector and Sentence Transformers; Philixa Brain is a Siri-like hands-free assistant for client queries, new-client creation, and key workflow control by voice using Deepgram STT, RAG retrieval, and Sarvam TTS.'),
        bullet('Built switchable local faster-whisper + pyannote diarization and Deepgram cloud transcription; used Redis/ARQ idempotent background jobs for transcription, embeddings, and reminder delivery, including WhatsApp pre-meeting briefings with prior context, commitments, and pending actions.'),
    ]),
    Spacer(1, 1.5),
    KeepTogether([
        project('Customer Retention AI System | 2025'),
        stack('Python, XGBoost, Scikit-learn, SMOTE, FastAPI'),
        links('<a href="https://shouryasingh-customer-churn-prediction.hf.space/ui"><u>Live Demo</u></a>  |  <a href="https://github.com/shouryasingh-codes/customer-churn-prediction"><u>GitHub</u></a>'),
        bullet('Built and deployed a churn-prediction REST API that returns churn probability, risk tier, and a suggested retention action; documented the interface through Swagger UI.'),
    ]),
    Spacer(1, 1.5),
    KeepTogether([
        project('SAVIOUR - AI Communication Simulator | 2026'),
        stack('Python, XGBoost, LLM Integration, NLP Feature Engineering | <font color="#1769E0"><a href="https://github.com/shouryasingh-codes/saviour"><u>GitHub</u></a></font>'),
        bullet('Built a four-step communication-training workflow covering assessment, level detection, live role simulation, and a coaching report with AI-rewritten answers.'),
    ]),
    section('TECHNICAL SKILLS'),
    P('<b>Languages:</b> Python, SQL, C++', 'RSkill'),
    P('<b>AI / LLM:</b> LLM APIs, RAG, semantic search, provider routing, prompt engineering, Hinglish NLP', 'RSkill'),
    P('<b>Backend:</b> FastAPI, Pydantic v2, SQLAlchemy ORM, REST APIs, WebSocket, Alembic', 'RSkill'),
    P('<b>Data &amp; Async:</b> PostgreSQL, pgvector, Redis, MinIO, ARQ job queues', 'RSkill'),
    P('<b>Voice / ML:</b> faster-whisper, Deepgram, Sarvam TTS, pyannote.audio diarization, AudioWorklet, Web Speech API, XGBoost, Scikit-learn, SMOTE, Sentence Transformers', 'RSkill'),
    P('<b>Delivery:</b> Docker, Render, Git/GitHub, pytest, httpx', 'RSkill'),
    section('EDUCATION'),
    P('Bachelor of Computer Applications (BCA) | Suresh Gyan Vihar University, Jaipur | Expected 2027', 'RBody'),
]

SimpleDocTemplate(str(out), pagesize=A4, leftMargin=0.54*inch, rightMargin=0.54*inch, topMargin=0.42*inch, bottomMargin=0.38*inch).build(story)
