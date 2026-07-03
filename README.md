# Multi-Agent Content Pipeline (Gemini)

A small Python project that chains three role-specific LLM "agents" to draft and
then self-review short content, built on the **Google GenAI SDK** with the
**Gemini 2.5 Flash** model. It is a personal learning project exploring
multi-agent orchestration and API token / cost tracking.

## How it works

The pipeline runs three agents in sequence:

1. **Researcher agent** gathers factual points, run at a low temperature (0.0) for accuracy.
2. **Editor agent** turns the research into an engaging newsletter, run at a higher temperature (0.7).
3. **Critic agent** reviews the draft and gives it a 1-5 star rating with feedback (temperature 0.2).

The token-tracking version also reads the API's `usage_metadata` after the run to
report total input tokens and any tokens saved through Gemini's implicit context caching.

## Project structure

| File | Purpose |
|------|---------|
| `multi_agent.py` | Core pipeline with the three agents |
| `multi_agent_token.py` | Same pipeline, plus token / context-caching metrics |
| `requirements.txt` | Python dependencies |

## Setup

1. Clone and install dependencies:
   ```bash
   git clone https://github.com/DharanidharPonnada/multi-agent-gemini-pipeline.git
   cd multi-agent-gemini-pipeline
   pip install -r requirements.txt
   ```

2. Set your Gemini API key as an environment variable (never hard-code it):
   ```bash
   # macOS / Linux
   export GEMINI_API_KEY="your_key_here"
   ```
   ```powershell
   # Windows
   setx GEMINI_API_KEY "your_key_here"
   ```

## Run

```bash
python multi_agent.py
```
The script will prompt you to enter a topic, then run the three agents in sequence.

To see token usage and context-caching metrics, run the tracking version instead:
```bash
python multi_agent_token.py
```

## Notes

- The API key is read from the `GEMINI_API_KEY` environment variable, so no credentials are committed to the repo.
- Built with the Google GenAI SDK (`google-genai`) and the Gemini 2.5 Flash model.

## Status

Personal project, built for learning and experimentation.
