"""
temperature_test.py - See how temperature affects responses
Purpose: Understand the impact of temperature on output randomness
"""
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Same prompt, different temperatures
prompt = "Write a creative one-sentence story about a robot."
temperatures = [0, 0.7, 1.5]
for temp in temperatures:
    print(f"\n{'='*60}")
    print(f"TEMPERATURE: {temp}")
    print('='*60)
    
    response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {"role": "system", "content": "You are a creative writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=temp,
        max_tokens=100
    )
    
    print(response.choices[0].message.content)
    print(f"\nTokens used: {response.usage.total_tokens}")
print("\n" + "="*60)
print("OBSERVATION: Notice how temperature=0 is consistent,")
print("while temperature=1.5 is more creative/unpredictable")
print("="*60)
