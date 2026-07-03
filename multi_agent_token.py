import os
from google import genai
from google.genai import types

# =====================================================================
# 1. INITIALIZATION & SECURITY SETUP
# =====================================================================
# The API key is read from an environment variable, so it is never stored
# in this file and can never be committed to GitHub by accident.
# Set it before running:
#   macOS / Linux : export GEMINI_API_KEY="your_key_here"
#   Windows       : setx GEMINI_API_KEY "your_key_here"
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise SystemExit("Please set the GEMINI_API_KEY environment variable before running.")

# Connect to the Google GenAI Client using the Gemini 2.5 Flash model
client = genai.Client(api_key=API_KEY)
MODEL_ID = 'gemini-2.5-flash'


# =====================================================================
# 2. AGENT DEFINITIONS
# =====================================================================

def run_researcher_agent(topic: str) -> str:
    """
    Agent 1: The Researcher.
    Gathers highly specific, factual background data using a low temperature
    for crisp, objective accuracy.
    """
    print("\n🕵️  Researcher Agent is gathering facts...")

    system_instruction = (
        "You are an expert technical researcher. Provide 3-4 deep, highly specific, "
        "and accurate facts about the user's topic. Avoid fluff or introductory commentary."
    )

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=f"Research this topic thoroughly: {topic}",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.0  # Zero temperature keeps the agent strictly focused on facts
        )
    )
    return response.text


def run_editor_agent(research_text: str) -> str:
    """
    Agent 2: The Editor.
    Transforms raw research data into a high-engagement newsletter post.
    """
    print("✍️  Editor Agent is writing the newsletter...")

    system_instruction = (
        "You are a world-class copywriter. Take the provided research facts and "
        "turn them into an engaging, punchy LinkedIn newsletter. Use emojis, clear headers, "
        "and an inviting tone. End with a call to action asking for comments."
    )

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=f"Transform this research into a post:\n\n{research_text}",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7  # Higher temperature allows for creative writing flair
        )
    )
    return response.text


# =====================================================================
# 3. INTERACTIVE ORCHESTRATION PIPELINE (WITH TOKEN TRACKING)
# =====================================================================
if __name__ == "__main__":
    print("🤖 Welcome to the Gemini Multi-Agent Orchestrator!")
    print("=" * 60)

    # Accepts the target topic dynamically from your terminal input prompt
    user_topic = input("✍️  Enter a tech topic you want the agents to process: ")

    print("\n" + "=" * 60)
    print(f"Starting Multi-Agent Workflow for: '{user_topic}'")
    print("=" * 60)

    # Step 1: Research
    raw_research = run_researcher_agent(user_topic)
    print("\n--- [Researcher Output] ---\n", raw_research)
    print("=" * 60)

    # Step 2: Edit / Copywrite
    final_newsletter = run_editor_agent(raw_research)
    print("\n--- [Final Editor Product] ---\n", final_newsletter)
    print("=" * 60)

    # Step 3: Review / Evaluate (run inline here to capture token usage metadata)
    print("🧐 Editor-in-Chief Agent is reviewing the post...")
    critic_instruction = (
        "You are a strict Editor-in-Chief. Review the provided newsletter draft. "
        "Provide a 1-5 star rating and a 2-sentence piece of feedback on whether "
        "the tone matches social media best practices. Do not rewrite the post, just critique it."
    )

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=f"Review this draft:\n\n{final_newsletter}",
        config=types.GenerateContentConfig(
            system_instruction=critic_instruction,
            temperature=0.2  # Low temperature ensures reliable, objective grading
        )
    )

    print("\n--- [Editor-in-Chief Review] ---\n", response.text)
    print("=" * 60)

    # =====================================================================
    # 4. TOKEN EFFICIENCY & CONTEXT CACHING MONITORING
    # =====================================================================
    print("\n📊 PIPELINE PERFORMANCE METRICS:")

    # Read response usage metadata to inspect implicit context caching
    cached_tokens = getattr(response.usage_metadata, 'cached_content_token_count', 0) or 0
    total_input = response.usage_metadata.prompt_token_count

    print(f" 🔹 Total Pipeline Input Tokens: {total_input}")
    print(f" 🔹 Cached Tokens (Saved Memory): {cached_tokens}")

    if cached_tokens > 0:
        savings_percentage = (cached_tokens / total_input) * 100
        print(f" 🎉 Context Caching saved {savings_percentage:.1f}% on input processing costs!")
    else:
        print(" 💡 Tip: Running repetitive prompts sequentially uses Gemini's implicit context caching.")

    print("=" * 60)
    print("\n✅ Workflow complete! Ready for your next run.")
