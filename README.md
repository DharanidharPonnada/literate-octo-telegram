# Multi-Agent Content Pipeline (Gemini)

A small Python project that chains three role-specific LLM "agents" to draft and
then self-review short content, built on the **Google GenAI SDK** with **Gemini**
models. It is a personal learning project exploring multi-agent orchestration and
API token / cost tracking.

## How it works

The pipeline runs three agents in sequence:

1. **Researcher agent** gathers factual points, run at a low temperature (~0.0) for accuracy.
2. **Editor agent** turns the research into engaging copy, run at a higher temperature (~0.7).
3. **Critic agent** reviews the draft and scores it for quality.

Token usage is read from the API's `usage_metadata` so you can observe context
caching and keep an eye on API cost.

## Project structure

| File | Purpose |
|------|---------|
| `multi_agent.py` | Core pipeline with the three agents |
| `multi_agent_token.py` | Variant that tracks token / usage_metadata |
| `tasks.sample.json` | Example input tasks |
| `requirements.txt` | Python dependencies |

## Setup

1. Clone and install dependencies:
   ```bash
   git clone https://github.com/DharanidharPonnada/multi-agent-gemini-pipeline.git
   cd multi-agent-gemini-pipeline
   pip install -r requirements.txt
   ```

2. Set your API key as an environment variable (never hard-code it):
   ```bash
   # macOS / Linux
   export GEMINI_API_KEY="your_key_here"
   ```
   ```powershell
   # Windows
   setx GEMINI_API_KEY "your_key_here"
   ```
   Use whichever variable name your code actually reads (for example `GOOGLE_API_KEY`).

3. Create your task file from the sample:
   ```bash
   cp tasks.sample.json tasks.json
   ```

## Run

```bash
python multi_agent.py
```
_If your entry script has a different name (for example `run_agent.py`), use that instead._

## Notes

- API keys are read from environment variables, so no credentials are committed to the repo.
- Built with the Google GenAI SDK (`google-genai`) and Gemini models.

## Status

Personal project, built for learning and experimentation.
