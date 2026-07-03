from google import genai
from google.genai import types

# 1. Put your API key right here inside the quotes
API_KEY = "ADD API KEY HERE"

# 2. Pass the key directly into the Gemini client setup
client = genai.Client(api_key=API_KEY)
MODEL_ID = 'gemini-2.5-flash'

def run_researcher_agent(topic: str) -> str:
    print("🕵️‍♂️ Researcher Agent is gathering facts...")
    system_instruction = "You are an expert technical researcher. Find 3-4 deep, specific bulleted facts."
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=f"Research this topic: {topic}",
        config=types.GenerateContentConfig(system_instruction=system_instruction, temperature=0.3)
    )
    return response.text

def run_editor_agent(research_notes: str) -> str:
    print("✍️ Editor Agent is writing the newsletter...")
    system_instruction = "You are a charismatic tech journalist. Turn raw notes into a fun LinkedIn post using emojis."
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=f"Turn these notes into a newsletter:\n\n{research_notes}",
        config=types.GenerateContentConfig(system_instruction=system_instruction, temperature=0.7)
    )
    return response.text

if __name__ == "__main__":
    user_topic = "The rise of Quantum Computing in 2026"
    print(f"Starting Multi-Agent Workflow for: '{user_topic}'\n" + "="*50)
    
    raw_research = run_researcher_agent(user_topic)
    print("\n--- [Researcher Output] ---\n", raw_research)
    
    final_newsletter = run_editor_agent(raw_research)
    print("\n--- [Final Editor Product] ---\n", final_newsletter)
    
