import os
from google import genai
from google.genai import types

# =====================================================================
# 1. INITIALIZATION & SECURITY SETUP
# =====================================================================
# SECURE SETUP: Replace the text inside the quotes below with your real API key
# When you push to GitHub, leave it as a placeholder to keep your account safe!
API_KEY = "YOUR_GEMINI_API_KEY_HERE"

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
    print("\n🕵️‍♂️ Researcher Agent is gathering facts...")
    
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
    Transforms raw research data into a high-engagement social media post.
    """
    print("✍️ Editor Agent is writing the newsletter...")
    
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


def run_critic_agent(newsletter_draft: str) -> str:
    """
    Agent 3: The Critic (Editor-in-Chief).
    Reviews the draft post, provides a rating, and offers optimization feedback.
    """
    print("🧐 Editor-in-Chief Agent is reviewing the post...")
    
    system_instruction = (
        "You are a strict Editor-in-Chief. Review the provided newsletter draft. "
        "Provide a 1-5 star rating and a 2-sentence piece of feedback on whether "
        "the tone matches social media best practices. Do not rewrite the post, just critique it."
    )
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=f"Review this draft:\n\n{newsletter_draft}",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2  # Low temperature ensures reliable, objective grading
        )
    )
    return response.text


# =====================================================================
# 3. INTERACTIVE ORCHESTRATION PIPELINE
# =====================================================================
if __name__ == "__main__":
    print("🤖 Welcome to the Gemini Multi-Agent Orchestrator!")
    print("=" * 60)
    
    # Halts execution and dynamically accepts your target topic directly from the terminal prompt
    user_topic = input("✍️ Enter a tech topic you want the agents to process: ")
    
    print("\n" + "=" * 60)
    print(f"Starting Multi-Agent Workflow for: '{user_topic}'")
    print("=" * 60)
    
    # Pipeline Execution: Step 1 (Research)
    raw_research = run_researcher_agent(user_topic)
    print("\n--- [Researcher Output] ---\n", raw_research)
    print("=" * 60)
    
    # Pipeline Execution: Step 2 (Edit/Copywrite)
    final_newsletter = run_editor_agent(raw_research)
    print("\n--- [Final Editor Product] ---\n", final_newsletter)
    print("=" * 60)
    
    # Pipeline Execution: Step 3 (Review/Evaluate)
    critic_review = run_critic_agent(final_newsletter)
    print("\n--- [Editor-in-Chief Review] ---\n", critic_review)
    print("=" * 60)
    print("\n✅ Workflow complete! Ready for your next run.")
