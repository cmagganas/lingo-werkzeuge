# OpenAI Realtime Console with Arcade (Spotify) Integration

This is a fork of the OpenAI Realtime Console example that adds an experimental Arcade AI tool integration for Spotify search. It otherwise preserves the same real-time voice/text chat workflow with GPT-4, WebRTC, React/Vite on the frontend, and FastAPI/Fastify on the backend.

---

## Purpose

- Provide real-time voice and text conversations powered by GPT-4o  
- Automatically detect music-related queries and invoke the `Spotify.Search` tool via Arcade AI  
- Populates the chat with Spotify search results (tracks, artists, playlists) when relevant  

> **Note:** This branch relies on an older Arcade API surface for Spotify and may no longer function end-to-end.

---

## Installation

### Prerequisites

- Node.js (16+)
- Python 3.12+
- OpenAI API key
- Arcade API key & registered email
- Spotify Client ID / Secret

### 1) Clone & Env Setup

```bash
git clone https://github.com/your-org/openai-realtime-console.git
cd openai-realtime-console

cp .env.example .env
python -m venv arcade_env
source arcade_env/bin/activate
```

### 2) Populate `.env`

```dotenv
OPENAI_API_KEY=sk-…
ARCADE_API_KEY=ak-…
ARCADE_EMAIL=you@example.com

# Spotify credentials for the Arcade Spotify.Search tool
SPOTIFY_CLIENT_ID=<your client ID>
SPOTIFY_CLIENT_SECRET=<your client secret>
```

### 3) Install Dependencies

```bash
npm install
pip install -r requirements.txt
```

---

## Running the Servers

You can use the provided helper script:

```bash
chmod +x start-servers.sh
./start-servers.sh
```

Or start each manually:

- **Backend (Arcade bridge)**  

  ```bash
  uvicorn arcade_bridge:app --reload --port 8000
  ```

- **Frontend / API proxy**  

  ```bash
  npm run dev
  ```

Open your browser to [http://localhost:3000](http://localhost:3000).

---

## How It Works

1. **Client** sends real-time messages to the Fastify server  
2. Fastify proxies chat messages to the OpenAI Realtime API  
3. If the GPT response contains a `tool_call` of type `Spotify.Search`, the FastAPI (Arcade bridge) endpoint at `/process` picks it up  
4. The bridge uses `arcadepy.Arcade().tools.execute("Spotify.Search", …)`  
5. The returned Spotify results are fed back into a second GPT pass to render user-friendly output  

---

## Key Code Examples

### 1) System Prompt & Tool Invocation  

```python
# openai-realtime-console/arcade_bridge.py

response = await openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system",
       "content": "You are a helpful assistant. When users ask about music or Spotify, use the Spotify.Search tool to find relevant results. For other queries, respond normally without using tools."},
      {"role": "user", "content": message.content}
    ],
    user=message.user_id,
    tools=["Spotify.Search"],
    tool_choice="auto"
)
```

### 2) Executing the Detected Spotify Tool Call  

```python
# openai-realtime-console/arcade_bridge.py

if tool_calls:
    tool_response = arcade_client.tools.execute(
      tool_name=tool_calls[0]["function"]["name"],
      inputs=tool_calls[0]["function"]["arguments"],
      user_id=message.user_id
    )
    # wrap and feed back into GPT…
```

### 3) Proxying from Fastify → FastAPI  

```js
// openai-realtime-console/server.js

server.post("/arcade", async (request, reply) => {
  const last = request.body.messages.length - 1;
  const response = await fetch("http://127.0.0.1:8000/process", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      content: request.body.messages[last].content,
      user_id: process.env.ARCADE_EMAIL
    })
  });
  return await response.json();
});
```

---

## Limitations & Troubleshooting

- **Non-functional**: The Spotify tool integration was built against an earlier Arcade API—Arcade’s OAuth/Spotify workflow has changed.  
- Ensure you’ve populated both `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`.  
- Check logs in both terminals (FastAPI & Fastify) for detailed errors.

---

> This document should serve as context for the modified branch. You can share or embed it in your own README or project documentation.
