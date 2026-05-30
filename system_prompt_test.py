"""
system_prompt_test.py - See how system prompts affect behavior
Purpose: Understand the power of persona/role assignment
"""
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Same question, different system prompts
question = "Should I invest in cryptocurrency?"
system_prompts = [
    "You are a conservative financial advisor who prioritizes safety.",
    "You are an aggressive risk-taking investor who loves speculation.",
    "You are a neutral financial educator who presents both sides."
]
for i, sys_prompt in enumerate(system_prompts, 1):
    print(f"\n{'='*60}")
    print(f"SYSTEM PROMPT {i}:")
    print(sys_prompt)
    print('='*60)
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.7,
        max_tokens=150
    )
    
    print("\nRESPONSE:")
    print(response.choices[0].message.content)
    print(f"\nTokens: {response.usage.total_tokens}")
print("\n" + "="*60)
print("OBSERVATION: Same question, different personas = different advice")
print("="*60)
