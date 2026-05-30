"""
test_cases.py - Define test cases for LLM evaluation
Purpose: Centralized test case definitions
"""

TEST_CASES = [
    {
        "id": "test_001",
        "name": "Factual Accuracy - Simple Math",
        "system_prompt": "You are a helpful assistant.",
        "user_prompt": "What is 15 + 27?",
        "expected_behavior": "Should return 42 without explanation",
        "category": "accuracy"
    },
    {
        "id": "test_002",
        "name": "Format Compliance - Haiku",
        "system_prompt": "You are a creative poet.",
        "user_prompt": "Write a haiku about artificial intelligence. Follow the 5-7-5 syllable structure exactly.",
        "expected_behavior": "Should be exactly 3 lines with 5-7-5 syllables",
        "category": "format"
    },
    {
        "id": "test_003",
        "name": "Tone Appropriateness - ELI5",
        "system_prompt": "You are a patient teacher who explains things to 5-year-olds.",
        "user_prompt": "Explain how a computer works.",
        "expected_behavior": "Should use simple language, no jargon, friendly tone",
        "category": "tone"
    },
    {
        "id": "test_004",
        "name": "Hallucination Detection - Fake Facts",
        "system_prompt": "You are a helpful assistant.",
        "user_prompt": "Tell me about the famous scientist Dr. Zephyr Quantum who invented the flux capacitor in 1955.",
        "expected_behavior": "Should recognize this is fictional and NOT make up information",
        "category": "hallucination"
    },
    {
        "id": "test_005",
        "name": "Instruction Following - JSON Output",
        "system_prompt": "You are a precise assistant who follows instructions exactly.",
        "user_prompt": "Extract the key information and return ONLY valid JSON with keys: name, age, city. Text: 'John is 25 years old and lives in Chicago.'",
        "expected_behavior": "Should return valid JSON with no extra text",
        "category": "format"
    }
]