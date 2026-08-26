# Original User Request

## Initial Request — 2026-08-26T18:10:11Z

# Teamwork Project Prompt — Draft

> Status: Launched
> Goal: Delegate to teamwork_preview and monitor progress
> Requested team: Expert AI Research Team

Conduct internet research on the definitive pre-deployment checklist for an enterprise-grade AI CRM (FastAPI, LangGraph, pgvector, Redis, WebSockets, JWT). Then, evaluate the provided `README.md` file to identify what the candidate still needs to implement or verify before safely deploying the Philixa 6.0 system to production. **CRITICAL RESTRICTION: Do not analyze, read, or evaluate any project code files or directories. Rely ONLY on internet research regarding modern deployment standards and the `README.md` file.**

Working directory: c:\Users\admin\Documents\philixa 6.0 2
Integrity mode: development

## Requirements

### R1. Deployment Standards Research
Search the web for current best practices, security requirements, and pre-flight checklists for deploying distributed AI applications (FastAPI + PostgreSQL/pgvector + LangGraph + WebSockets) to production in 2026.

### R2. README Gap Analysis
Read the `README.md` file in the working directory (do not read any other code files). Compare the documented architecture and features against the deployment checklist generated in R1. Identify what critical deployment steps, security hardeners, or infrastructure configurations are currently missing or need to be done.

### R3. Output Report
Produce a concise Markdown report (`pre_deployment_checklist.md`) detailing:
1. The standard deployment checklist for this tech stack.
2. What the Philixa project already has (based on the README).
3. The exact steps the user must complete before safely deploying this project to a cloud provider.

## Acceptance Criteria

### Verification
- [ ] `pre_deployment_checklist.md` is generated in the project root.
- [ ] The report explicitly identifies missing deployment steps based solely on the README.
- [ ] Zero code files (Python, Dockerfiles, etc.) are read or analyzed.
- [ ] Agent-as-judge: A separate agent independently reviews the report to ensure no codebase analysis was performed and the advice is grounded in current internet deployment standards.

## Follow-up — 2026-08-26T18:52:47Z

# Teamwork Project Prompt — Draft

> Status: Launched
> Goal: Delegate to teamwork_preview and monitor progress
> Requested team: [none — teamwork routes from the description]

Read the `100_user_deployment_fixes.md` report to understand the 24 required deployment fixes. Then, analyze the project codebase and data flow to determine exactly which files and lines of code need to be modified for each fix. Finally, create a strict step-by-step implementation plan (from Fix 1 to Fix 24) detailing the exact file modifications required. Do not apply the fixes yet; only create the actionable plan.

Working directory: c:\Users\admin\Documents\philixa 6.0 2
Integrity mode: development

## Requirements

### R1. Report & Codebase Analysis
Read `100_user_deployment_fixes.md`. Then, thoroughly analyze the project files (FastAPI routers, core configs, frontend scripts, database models) to understand the current data flow and map each of the 24 fixes to its corresponding codebase location.

### R2. Sequential Implementation Plan
Design a strict, step-by-step execution plan ordering the fixes logically from 1 to 24. For each step, explicitly state:
- The goal of the fix.
- The exact file path(s) to be modified.
- The specific code or configuration changes required.

### R3. Output
Produce a detailed Markdown document (`24_fixes_implementation_plan.md`) containing the step-by-step plan. Ensure the plan explicitly warns against implementing everything at once, advocating for a sequential 1-by-1 approach.

## Acceptance Criteria

### Verification
- [ ] `24_fixes_implementation_plan.md` is generated in the project root.
- [ ] Every one of the 24 fixes is mapped to a specific file in the repository.
- [ ] The plan is ordered sequentially (Step 1 to Step 24).
- [ ] Agent-as-judge: A separate agent independently reviews the plan to ensure the file mappings are accurate based on the actual codebase structure.

## Follow-up — 2026-08-26T19:12:58Z

# Teamwork Project Prompt — Draft

> Status: Launched
> Goal: Delegate to teamwork_preview and monitor progress
> Requested team: [none — teamwork routes from the description]

Read `24_fixes_implementation_plan.md` and execute ONLY the top 3 critical fixes that prevent app crashes. Ignore all other fixes. This is a fast-track deployment strategy.

Working directory: c:\Users\admin\Documents\philixa 6.0 2
Integrity mode: development

## Requirements

### R1. Fast-Track Fix Selection
From the 24-step plan, you must execute ONLY the following three steps:
1. **Step 1:** Production Multi-Worker Process Manager (Gunicorn)
2. **Step 3:** Request Payload Upload Ceiling (10MB Limit)
3. **Step 5:** Bounded Database Connection Pooling & Pre-Ping Verification

### R2. Code Modification
Apply the exact code changes specified in the plan for these three steps (e.g., modifying `Dockerfile`, `docker-compose.yml`, `requirements.txt`, `routes_audio.py`, `main.py`, `session.py`, and `config.py`).

### R3. Ignore Remaining Steps
Do not apply Step 2, Step 4, or Steps 6 through 24. We are skipping them intentionally to save time.

## Acceptance Criteria

### Verification
- [ ] Gunicorn is added to `requirements.txt`, `Dockerfile`, and `docker-compose.yml` (Step 1).
- [ ] 10MB payload ceiling is added to `routes_audio.py` and `main.py` middleware (Step 3).
- [ ] Database connection pool settings (`pool_size=15`, etc.) are added to `session.py` and `config.py` (Step 5).
- [ ] Agent-as-judge: A separate agent independently reviews `git diff` to ensure ONLY files related to these 3 steps were modified, and nothing else.

## Follow-up — 2026-08-26T19:49:44Z

# Teamwork Project Prompt — Draft

> Status: Launched
> Goal: Delegate to teamwork_preview and monitor progress
> Requested team: [none — teamwork routes from the description]

Conduct comprehensive internet research on the current market (as of today) to determine the absolute cheapest, yet crash-proof, deployment strategies for a heavy AI application (PyTorch, Whisper, LangGraph, FastAPI) serving 50-100 concurrent users. 

Working directory: c:\Users\admin\Documents\philixa 6.0 2
Integrity mode: development

## Requirements

### R1. Strictly Research Only
DO NOT write any code, DO NOT modify the codebase, and DO NOT run any deployment commands. Your task is strictly limited to internet research.

### R2. Cost vs. Stability Analysis
Analyze our current setup (Docker Compose, Gunicorn with 2-4 workers, PostgreSQL, Redis, MinIO on a single monolithic server) vs. alternative cheap cloud architectures (e.g., serverless GPUs, managed API services like Groq/RunPod/Modal, cheap VPS providers like Hetzner vs AWS). 

### R3. Deliverable
Produce a markdown report (`cheapest_deployment_research.md`) that answers:
1. Is our current monolithic Docker setup the absolute cheapest way to support 50-100 users without crashing?
2. If not, what is the exact alternative architecture that is cheaper and crash-proof? Include current market pricing and specific provider names.

## Acceptance Criteria

### Verification
- [ ] No files in the codebase are modified.
- [ ] A new file `cheapest_deployment_research.md` is created containing current market research and cost comparisons.
- [ ] The research specifically addresses heavy AI workloads (PyTorch/Whisper) rather than standard web apps.
- [ ] Agent-as-judge: A separate agent verifies that the report contains real, current market data and provider pricing from internet searches.
