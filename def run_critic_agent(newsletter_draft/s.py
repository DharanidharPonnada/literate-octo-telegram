def run_critic_agent(newsletter_draft: str) -> str:
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
            temperature=0.2 # Low temperature for consistent grading logic
        )
    )
    return response.text
# ... (Keep researcher and editor code execution above this)
    final_newsletter = run_editor_agent(raw_research)
    print("\n--- [Final Editor Product] ---\n", final_newsletter)
    print("="*50)
    
    # 3rd Agent Execution: Hand off the final newsletter directly to the critic
    critic_review = run_critic_agent(final_newsletter)
    print("\n--- [Editor-in-Chief Review] ---\n", critic_review)
