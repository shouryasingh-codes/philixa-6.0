<div align="center">
  <h1>🚀 Philixa 6.0</h1>
  <p><b>The Agentic AI-First CRM for Modern Relationship Managers</b></p>
  
  [![FastAPI](https://img.shields.io/badge/Backend-FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
  [![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%20%2B%20pgvector-316192?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)
  [![AI](https://img.shields.io/badge/AI-LangGraph%20%7C%20LiteLLM-blueviolet?style=for-the-badge)]()
  [![Docker](https://img.shields.io/badge/Infrastructure-Docker-2496ED?style=for-the-badge&logo=docker)]()
</div>

<br/>

## 📖 About The Project
Philixa 6.0 is an enterprise-grade Customer Relationship Management (CRM) platform that eliminates manual data entry. Built for Financial Advisors, Real Estate Agents, and B2B Account Executives, it uses Voice AI to transcribe meetings and an Agentic Copilot to query your database in natural language.

<details>
  <summary><strong>Table of Contents (Click to expand)</strong></summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#core-features">Core Features</a></li>
    <li><a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

---

## ✨ Core Features
*   **🎙️ Zero-Latency Voice AI:** Live browser dictation (Web Speech API) and speaker-diarized meeting capture (Deepgram STT).
*   **🧠 Agentic Portfolio Copilot:** Query your portfolio in natural language. Powered by LangGraph for SQL generation and pgvector for semantic search.
*   **🛡️ Role-Based Access Control (RBAC):** Strict data segregation. Owners see team analytics; employees see their own clients.
*   **📊 Proactive Risk Management:** AI automatically extracts commitments, due dates, and client risk signals from meeting audio.

---

## 🚀 Getting Started
To get a local copy up and running follow these simple steps.

### Prerequisites
*   Docker & Docker Compose
*   Groq API Key (for LLM inference)

### Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/philixa.git
   ```
2. Setup environment variables:
   ```bash
   cp .env.example .env
   ```
   Add your `PHILIXA_GROQ_API_KEY` to the `.env` file.
3. Boot the Docker infrastructure (PostgreSQL, Redis, MinIO, FastAPI):
   ```bash
   docker-compose up --build
   ```

---

## 💻 Usage
Once the server is running at `http://localhost:8000`, you can interact with the API or UI.

**Example API Request (Copilot):**
```bash
curl -X POST "http://localhost:8000/api/v1/dashboard/copilot/ask" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: dev-api-key" \
     -d '{"question": "How many clients do I have?"}'
```

---

## 🗺️ Roadmap
- [x] Voice STT Integration (Deepgram)
- [x] Multi-tenant RBAC Security
- [x] Agentic Portfolio Copilot (LangGraph)
- [ ] Migrate Vanilla JS to React/Next.js
- [ ] Stripe Billing Integration
- [ ] Cloud Deployment (AWS/Vercel)

---

## 🤝 Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---

## 📬 Contact
Project Link: [https://github.com/your-username/philixa](https://github.com/your-username/philixa)
