# Taskade PDF-to-Notes

Upload PDFs to a Taskade AI Agent's knowledge base and get AI-generated
notes, summaries, and chunked insights back.

## What is Taskade?

Taskade is a project-management + AI platform.  Its AI Agents can ingest
documents (PDFs, DOCX, TXT, …) as knowledge sources and then answer
questions about them, summarise them, and extract action items.

**Free plan**: generous — includes AI agents and document upload.

---

## ⚠️  API Key Required

Taskade uses a personal access token.  There is no anonymous/free-tier
REST access without an account.

### How to get your key (5 minutes, free account)

1. Sign up at <https://www.taskade.com> (free plan available)
2. Go to **Settings → Developer → Personal Access Tokens**
3. Click **Generate New Token**, name it anything (e.g. `pdf-demo`)
4. Copy the token — you will only see it once

### Set the token

```bash
export TASKADE_API_KEY=td_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Or create a `.env` file (never commit this):

```
TASKADE_API_KEY=td_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TASKADE_AGENT_ID=agt_xxxxxxxxxxxx   # optional — auto-detected if omitted
```

---

## Quick start

```bash
cd /Users/j/APX/taskade
source venv/bin/activate
export TASKADE_API_KEY=<your-token>
python test.py
```

Without a key the script runs in **demo mode** and prints mock API
responses so you can see exactly what each call does.

---

## Python SDK situation

| Package | Status |
|---------|--------|
| `taskade` (PyPI 0.0.1) | **Unrelated** — it is a DAG task-executor library, not the Taskade.com API |
| `@taskade/sdk` (npm) | Official **TypeScript** SDK only |
| Python | Must use the **REST API** directly via `requests` |

`test.py` implements a minimal `TaskadeClient` that wraps the REST API.

---

## PDF → Notes workflow

```
User
 │
 ├─ 1. GET  /workspaces                      → workspace ID
 ├─ 2. GET  /workspaces/{id}/folders         → folder ID
 ├─ 3. GET  /folders/{id}/agents             → agent ID
 ├─ 4. POST api.taskade.com/v1/agents/{id}/knowledge/bulk
 │         multipart: files[]=(doc.pdf, …)  → media ID
 └─ 5. Open Taskade UI → ask agent questions about the PDF
```

The agent processes the PDF asynchronously and indexes it as a knowledge
chunk.  You can then query it:

- "Summarise this document"
- "Extract the key action items"
- "What are the main topics covered?"
- "Create bullet-point notes from section 2"

---

## REST API reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/workspaces` | List all workspaces |
| GET | `/workspaces/{id}/folders` | List folders |
| GET | `/folders/{id}/agents` | List AI agents |
| POST | `api.taskade.com/v1/agents/{id}/knowledge/bulk` | Upload file(s) |
| POST | `/agents/{id}/knowledge/media` | Add media by ID |
| GET | `/agents/{id}/convos/` | List conversations |
| GET | `/agents/{id}/convos/{convoId}` | Get conversation |

Full docs: <https://docs.taskade.com/docs/developers/developers/api>

---

## Files

```
taskade/
├── venv/               Python 3.14 virtual environment
├── requirements.txt    requests, python-dotenv
├── test.py             Full demo / live-test script
├── README.md           This file
└── .env.example        Template for credentials
```

---

## Packages installed

```
requests       2.34.2   HTTP client for REST API calls
python-dotenv  1.2.x    Load TASKADE_API_KEY from .env
taskade        0.0.1    (installed but unused — unrelated DAG library)
```
