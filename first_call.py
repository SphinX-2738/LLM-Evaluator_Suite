"""
first_call.py - Your first LLM API call
Purpose: Understand request/response structure and token usage
Author: Ankur
Date: Week 1, Day 1
"""
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

print("Making API call to Groq...")
print("=" * 60)

# Make your first API call
response = client.chat.completions.create(
    model="qwen/qwen3.6-27b",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI assistant who explains technical concepts clearly."
        },
        {
            "role": "user",
            "content": "Explain what a token is in LLMs in exactly 2 sentences."
        }
    ],
    temperature=0.7,
    max_tokens=150
)

# Extract the AI's response
ai_message = response.choices[0].message.content

# Display results
print("AI RESPONSE:")
print("=" * 60)
print(ai_message)
print("=" * 60)

# Display token usage (CRITICAL for cost tracking)
print("\n📊 TOKEN USAGE:")
print(f"   Input (prompt) tokens:  {response.usage.prompt_tokens}")
print(f"   Output (completion) tokens: {response.usage.completion_tokens}")
print(f"   Total tokens used: {response.usage.total_tokens}")
print("=" * 60)

# Display model info
print(f"\n🤖 Model used: {response.model}")
print(f"⏱️  Response ID: {response.id}")
print("=" * 60)