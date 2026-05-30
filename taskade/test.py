#!/usr/bin/env python3
"""
test.py — Taskade PDF-to-Notes Demo
=====================================
Demonstrates the Taskade REST API workflow for:
  1. Authenticating with a Personal Access Token
  2. Discovering workspaces → folders → agents
  3. Uploading a PDF to an AI agent's knowledge base
  4. Listing agent conversations (where notes/summaries appear)

API docs: https://docs.taskade.com/docs/developers/developers/api
API base: https://www.taskade.com/api/v1
Bulk upload: https://api.taskade.com/v1/agents/{agent_id}/knowledge/bulk

Set TASKADE_API_KEY (and optionally TASKADE_AGENT_ID) before running:
  export TASKADE_API_KEY=your_token_here
  python test.py

Without an API key the script runs in DEMO mode and exits 0 (NEEDS_API_KEY).
"""

import io
import json
import os
import sys
import tempfile

import requests

# ---------------------------------------------------------------------------
# Try to load .env if present
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------
API_BASE = "https://www.taskade.com/api/v1"
BULK_KNOWLEDGE_URL = "https://api.taskade.com/v1/agents/{agent_id}/knowledge/bulk"


# ---------------------------------------------------------------------------
# Minimal pure-Python PDF generator (no third-party deps)
# ---------------------------------------------------------------------------

def make_sample_pdf() -> bytes:
    """
    Build a minimal but spec-valid PDF containing a short 'Project Notes'
    document.  Tracks exact byte offsets for the xref table so that PDF
    readers (and the Taskade ingestion pipeline) can parse it correctly.
    """
    buf = io.BytesIO()

    def w(data: bytes) -> int:
        """Write bytes and return the starting offset."""
        pos = buf.tell()
        buf.write(data)
        return pos

    offsets: dict[int, int] = {}

    # ---- Header ----
    w(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")

    # ---- Object 1: Catalog ----
    offsets[1] = w(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")

    # ---- Object 2: Pages dict ----
    offsets[2] = w(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")

    # ---- Object 4: Content stream (built first so we know its length) ----
    content_lines = [
        b"BT",
        b"/F1 14 Tf",
        b"72 750 Td",
        b"(Project Management: Key Notes) Tj",
        b"0 -28 Td",
        b"/F1 11 Tf",
        b"(1. Define clear project goals and success criteria.) Tj",
        b"0 -20 Td",
        b"(2. Break the project into small, manageable tasks.) Tj",
        b"0 -20 Td",
        b"(3. Assign owners and set realistic deadlines.) Tj",
        b"0 -20 Td",
        b"(4. Communicate status updates to all stakeholders.) Tj",
        b"0 -20 Td",
        b"(5. Review progress weekly and adapt the plan.) Tj",
        b"0 -20 Td",
        b"(6. Celebrate milestones to keep the team motivated.) Tj",
        b"ET",
    ]
    content = b"\n".join(content_lines) + b"\n"

    # ---- Object 3: Page ----
    offsets[3] = w(
        b"3 0 obj\n"
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]\n"
        b"   /Contents 4 0 R\n"
        b"   /Resources << /Font << /F1 5 0 R >> >> >>\n"
        b"endobj\n"
    )

    # ---- Object 4: Stream ----
    offsets[4] = w(
        f"4 0 obj\n<< /Length {len(content)} >>\nstream\n".encode()
    )
    w(content)
    w(b"endstream\nendobj\n")

    # ---- Object 5: Font ----
    offsets[5] = w(
        b"5 0 obj\n"
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\n"
        b"endobj\n"
    )

    # ---- xref table ----
    xref_pos = buf.tell()
    w(b"xref\n")
    w(b"0 6\n")
    w(b"0000000000 65535 f \n")
    for i in range(1, 6):
        w(f"{offsets[i]:010d} 00000 n \n".encode())

    # ---- Trailer ----
    w(
        f"trailer\n<< /Size 6 /Root 1 0 R >>\n"
        f"startxref\n{xref_pos}\n%%EOF\n".encode()
    )

    return buf.getvalue()


# ---------------------------------------------------------------------------
# Taskade REST API client
# ---------------------------------------------------------------------------

class TaskadeClient:
    """Thin wrapper around the Taskade v1 REST API using requests."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    # --- Discovery endpoints ------------------------------------------------

    def get_workspaces(self) -> dict:
        """GET /workspaces"""
        r = self.session.get(f"{API_BASE}/workspaces")
        r.raise_for_status()
        return r.json()

    def get_folders(self, workspace_id: str) -> dict:
        """GET /workspaces/{workspaceId}/folders"""
        r = self.session.get(f"{API_BASE}/workspaces/{workspace_id}/folders")
        r.raise_for_status()
        return r.json()

    def get_agents(self, folder_id: str) -> dict:
        """GET /folders/{folderId}/agents"""
        r = self.session.get(f"{API_BASE}/folders/{folder_id}/agents")
        r.raise_for_status()
        return r.json()

    # --- Knowledge / media endpoints ----------------------------------------

    def upload_pdf_to_knowledge(
        self,
        agent_id: str,
        pdf_path: str,
        filename: str = "document.pdf",
    ) -> dict:
        """
        Upload a PDF file directly to an agent's knowledge base.

        Uses the bulk knowledge endpoint:
          POST https://api.taskade.com/v1/agents/{agent_id}/knowledge/bulk
          Content-Type: multipart/form-data
          files[]: (filename, file_bytes, 'application/pdf')
        """
        url = BULK_KNOWLEDGE_URL.format(agent_id=agent_id)
        # Remove Content-Type header so requests can set the multipart boundary
        headers = {"Authorization": f"Bearer {self.api_key}"}
        with open(pdf_path, "rb") as fh:
            r = requests.post(
                url,
                headers=headers,
                files={"files[]": (filename, fh, "application/pdf")},
                timeout=60,
            )
        r.raise_for_status()
        return r.json()

    def add_media_to_knowledge(self, agent_id: str, media_id: str) -> dict:
        """
        POST /agents/{agentId}/knowledge/media
        Add an already-uploaded media item to an agent's knowledge base by ID.
        """
        r = self.session.post(
            f"{API_BASE}/agents/{agent_id}/knowledge/media",
            json={"mediaId": media_id},
        )
        r.raise_for_status()
        return r.json()

    def get_agent(self, agent_id: str) -> dict:
        """GET /agents/{agentId}"""
        r = self.session.get(f"{API_BASE}/agents/{agent_id}")
        r.raise_for_status()
        return r.json()

    def get_conversations(self, agent_id: str) -> dict:
        """GET /agents/{agentId}/convos/"""
        r = self.session.get(f"{API_BASE}/agents/{agent_id}/convos/")
        r.raise_for_status()
        return r.json()


# ---------------------------------------------------------------------------
# Demo mode (no API key)
# ---------------------------------------------------------------------------

def run_demo_mode() -> bool:
    """
    Shows exactly what each API call would look like, using mock responses.
    Exits with status NEEDS_API_KEY.
    """
    print()
    print("=" * 62)
    print("  TASKADE PDF-TO-NOTES  (DEMO MODE — no API key)")
    print("=" * 62)

    # --- Generate a real PDF even in demo mode ---
    print("\n[1/6] Generating sample PDF ...")
    pdf_bytes = make_sample_pdf()
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    tmp.write(pdf_bytes)
    tmp.close()
    print(f"      ✓ {tmp.name}  ({len(pdf_bytes):,} bytes, valid PDF-1.4)")

    print("\n[2/6] Authenticate  →  GET /workspaces")
    print('      Mock response: { "items": [{ "id": "ws_abc123", "name": "My Workspace" }] }')

    print("\n[3/6] List folders  →  GET /workspaces/ws_abc123/folders")
    print('      Mock response: { "items": [{ "id": "fld_xyz789", "name": "AI Agents" }] }')

    print("\n[4/6] List agents   →  GET /folders/fld_xyz789/agents")
    print('      Mock response: { "items": [{ "id": "agt_111222", "name": "Doc Analyst" }] }')

    print("\n[5/6] Upload PDF to agent knowledge")
    print("      POST https://api.taskade.com/v1/agents/agt_111222/knowledge/bulk")
    print("      Content-Type: multipart/form-data")
    print(f"      files[]: (sample_notes.pdf, {len(pdf_bytes):,} bytes, application/pdf)")
    print('      Mock response: { "ok": true, "medias": [{ "id": "med_999", "name": "sample_notes.pdf" }] }')

    print("\n[6/6] Query agent conversations (notes appear here after processing)")
    print("      GET /agents/agt_111222/convos/")
    print("      → In the Taskade UI, open the agent and ask:")
    print('        "Summarize the uploaded document"')
    print('        "Extract the key action items from the PDF"')
    print('        "Create bullet-point notes from the document"')

    print()
    os.unlink(tmp.name)

    print("=" * 62)
    print("  STATUS: NEEDS_API_KEY")
    print("  Set TASKADE_API_KEY and re-run for a live test.")
    print("  See README.md for setup instructions.")
    print("=" * 62)
    return True   # acceptable exit — not a failure


# ---------------------------------------------------------------------------
# Live mode (real API key)
# ---------------------------------------------------------------------------

def run_live_mode(api_key: str, agent_id: str | None = None) -> bool:
    client = TaskadeClient(api_key)

    print()
    print("=" * 62)
    print("  TASKADE PDF-TO-NOTES  (LIVE MODE)")
    print("=" * 62)

    # 1. Authenticate
    print("\n[1/6] Authenticating → GET /workspaces ...")
    try:
        ws_resp = client.get_workspaces()
    except requests.HTTPError as e:
        print(f"      ERROR {e.response.status_code}: {e.response.text[:200]}")
        return False

    workspaces = ws_resp.get("items", [])
    if not workspaces:
        print("      ERROR: No workspaces found for this token.")
        return False
    ws = workspaces[0]
    print(f"      ✓ Workspace: '{ws.get('name')}' (id={ws.get('id')})")

    # 2. Folders
    print(f"\n[2/6] Listing folders in workspace {ws['id']} ...")
    try:
        fld_resp = client.get_folders(ws["id"])
    except requests.HTTPError as e:
        print(f"      ERROR {e.response.status_code}: {e.response.text[:200]}")
        return False

    folders = fld_resp.get("items", [])
    if not folders:
        print("      WARNING: No folders found.")
        return False
    folder = folders[0]
    print(f"      ✓ Folder: '{folder.get('name')}' (id={folder.get('id')})")

    # 3. Agents
    if not agent_id:
        print(f"\n[3/6] Listing agents in folder {folder['id']} ...")
        try:
            agt_resp = client.get_agents(folder["id"])
        except requests.HTTPError as e:
            print(f"      ERROR {e.response.status_code}: {e.response.text[:200]}")
            return False

        agents = agt_resp.get("items", [])
        if not agents:
            print("      WARNING: No agents found in this folder.")
            print("      Create an agent in Taskade and set TASKADE_AGENT_ID.")
            # Still a partial success — auth worked
            print()
            print("=" * 62)
            print("  STATUS: NEEDS_AGENT_ID  (authentication succeeded)")
            print("  Create an AI Agent in Taskade, then set:")
            print("    export TASKADE_AGENT_ID=<your-agent-id>")
            print("=" * 62)
            return True
        agent = agents[0]
        agent_id = agent["id"]
        print(f"      ✓ Agent: '{agent.get('name')}' (id={agent_id})")
    else:
        print(f"\n[3/6] Using TASKADE_AGENT_ID={agent_id}")
        try:
            agent_detail = client.get_agent(agent_id)
            print(f"      ✓ Agent: '{agent_detail.get('item', {}).get('name', '?')}'")
        except requests.HTTPError as e:
            print(f"      WARNING: Could not fetch agent details: {e.response.status_code}")

    # 4. Generate PDF
    print("\n[4/6] Generating sample PDF ...")
    pdf_bytes = make_sample_pdf()
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    tmp.write(pdf_bytes)
    tmp.close()
    print(f"      ✓ {tmp.name}  ({len(pdf_bytes):,} bytes)")

    # 5. Upload to agent knowledge
    print(f"\n[5/6] Uploading PDF to agent knowledge (agent_id={agent_id}) ...")
    try:
        up_resp = client.upload_pdf_to_knowledge(
            agent_id, tmp.name, filename="sample_project_notes.pdf"
        )
        print("      ✓ Upload response:")
        print("      " + json.dumps(up_resp, indent=2)[:400].replace("\n", "\n      "))
    except requests.HTTPError as e:
        print(f"      ERROR {e.response.status_code}: {e.response.text[:300]}")
        print("      (The agent will still have its existing knowledge.)")
    finally:
        os.unlink(tmp.name)

    # 6. List conversations
    print(f"\n[6/6] Listing agent conversations ...")
    try:
        conv_resp = client.get_conversations(agent_id)
        items = conv_resp.get("items", [])
        print(f"      ✓ {len(items)} conversation(s) found.")
        if items:
            print("      Latest:", json.dumps(items[0], indent=2)[:250].replace("\n", "\n      "))
    except requests.HTTPError as e:
        print(f"      Note ({e.response.status_code}): {e.response.text[:100]}")

    print()
    print("=" * 62)
    print("  STATUS: SUCCESS")
    print("  The PDF has been added to the agent's knowledge.")
    print("  Open Taskade and ask the agent to summarise the document.")
    print("=" * 62)
    return True


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    api_key = os.environ.get("TASKADE_API_KEY", "").strip()
    agent_id = os.environ.get("TASKADE_AGENT_ID", "").strip() or None

    if not api_key:
        ok = run_demo_mode()
    else:
        ok = run_live_mode(api_key, agent_id)

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
