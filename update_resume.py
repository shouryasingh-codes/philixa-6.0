from pathlib import Path
from shutil import copy2

from docx import Document


source = Path("output/Shourya_Singh_Resume_2026.docx")
target = Path("output/Shourya_Singh_Resume_Accurate_2026.docx")
copy2(source, target)

document = Document(target)
summary = document.paragraphs[3]
summary.text = (
    "Applied AI and backend developer building end-to-end LLM workflows, "
    "evidence-backed retrieval, voice-enabled copilots, and asynchronous Python services. "
    "Focused on reliable AI product features with validation, human review, "
    "and deployment-ready architecture."
)

document.save(target)
