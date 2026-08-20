from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether

OUT = Path('output/resume/Shourya_Singh_Resume_Updated_2026.pdf')
blue, dark, muted = HexColor('#1B4B78'), HexColor('#191919'), HexColor('#505050')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle('Name', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=17, leading=18, alignment=TA_CENTER, textColor=dark, spaceAfter=1))
styles.add(ParagraphStyle('Role', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.6, leading=11, alignment=TA_CENTER, textColor=blue, spaceAfter=1))
styles.add(ParagraphStyle('Contact', parent=styles['Normal'], fontName='Helvetica', fontSize=7.8, leading=9, alignment=TA_CENTER, textColor=dark, spaceAfter=3))
styles.add(ParagraphStyle('Section', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.4, leading=11, textColor=blue, spaceBefore=4, spaceAfter=1))
styles.add(ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=8.25, leading=9.7, textColor=dark, spaceAfter=1))
styles.add(ParagraphStyle('Project', parent=styles['Normal'], fontName='Helvetica', fontSize=8.8, leading=10.1, textColor=dark, spaceAfter=0))
styles.add(ParagraphStyle('ResumeBullet', parent=styles['Normal'], fontName='Helvetica', fontSize=8.05, leading=9.35, leftIndent=8, firstLineIndent=-6, textColor=dark, spaceAfter=0.55))
styles.add(ParagraphStyle('Skills', parent=styles['Normal'], fontName='Helvetica', fontSize=7.85, leading=9.15, textColor=dark, spaceAfter=0))

def P(text, style): return Paragraph(text, styles[style])
def header(title, stack='', links=''):
    parts = [f'<b>{title}</b>']
    if stack: parts.append(f'<font color="#505050"> | {stack}</font>')
    if links: parts.append(f'<font color="#1B4B78"> | {links}</font>')
    return P(''.join(parts), 'Project')
def bullet(t): return P('• ' + t, 'ResumeBullet')

story = [
    P('SHOURYA SINGH', 'Name'),
    P('Applied AI &amp; Backend Developer', 'Role'),
    P('+91 9610621152  |  shouryasingh3937@gmail.com  |  Jaipur, India  |  Open to Gurugram / Remote  |  LinkedIn  |  GitHub', 'Contact'),
    P('PROFESSIONAL SUMMARY', 'Section'),
    P('Applied AI and backend developer building end-to-end LLM workflows, evidence-backed retrieval, voice-enabled copilots, and asynchronous Python services. Focused on reliable AI product features with validation, human review, and deployment-ready architecture.', 'Body'),
    P('PROJECTS', 'Section'),
    KeepTogether([
        header('PHILIXA - AI Meeting Intelligence MVP for Financial Advisors', '2026', 'Live Demo | GitHub'),
        bullet('Built an end-to-end meeting-intelligence workflow for pasted notes, audio uploads, and live browser microphone input; extracts commitments, risks, client priorities, and follow-up context.'),
        bullet('Implemented economy-model-first extraction with Pydantic validation, escalation to a review model, manual-review fallback, and audit logs for model latency and estimated cost.'),
        bullet('Built evidence-backed client memory using pgvector and Sentence Transformers; semantic retrieval returns meeting dates and snippets for natural-language client questions.'),
        bullet('Engineered browser voice workflows with AudioWorklet/WebSocket streaming, faster-whisper/Deepgram transcription, Web Speech API fast dictation, and a Deepgram STT + Sarvam TTS assistant for hands-free client queries.'),
        bullet('Added organization/user-scoped client data, HITL client resolution, and opt-in WhatsApp reminders with delivery logs, idempotent Redis/ARQ jobs, retries, quiet hours, and rate limits.'),
    ]),
    Spacer(1, 1.5),
    KeepTogether([
        header('Customer Retention AI System', '2025', 'Live Demo | GitHub'),
        bullet('Built and deployed a churn-prediction REST API using XGBoost, Scikit-learn, and SMOTE; returns churn probability, risk tier, and a suggested retention action through Swagger UI.'),
    ]),
    Spacer(1, 1.5),
    KeepTogether([
        header('SAVIOUR - AI Communication Simulator', '2026', 'GitHub'),
        bullet('Built a four-step communication-training workflow covering assessment, level detection, live role simulation, and a coaching report with AI-rewritten answers.'),
    ]),
    P('TECHNICAL SKILLS', 'Section'),
    P('<b>Languages:</b> Python, SQL, C++', 'Skills'),
    P('<b>AI / LLM:</b> LLM APIs, RAG, semantic search, provider routing, prompt engineering, Hinglish NLP', 'Skills'),
    P('<b>Backend:</b> FastAPI, Pydantic v2, SQLAlchemy ORM, REST APIs, WebSocket, Alembic', 'Skills'),
    P('<b>Data &amp; Async:</b> PostgreSQL, pgvector, Redis, MinIO, ARQ job queues', 'Skills'),
    P('<b>Voice / ML:</b> faster-whisper, Deepgram, Sarvam TTS, pyannote.audio, AudioWorklet, Web Speech API, XGBoost, Scikit-learn, SMOTE, Sentence Transformers', 'Skills'),
    P('<b>Delivery:</b> Docker, Render, Git/GitHub, pytest, httpx', 'Skills'),
    P('EDUCATION', 'Section'),
    P('<b>Bachelor of Computer Applications (BCA)</b> | Suresh Gyan Vihar University, Jaipur | Expected 2027', 'Body'),
]

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=0.52*inch, rightMargin=0.52*inch, topMargin=0.38*inch, bottomMargin=0.38*inch)
doc.build(story)
