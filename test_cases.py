"""
test_cases.py - Comprehensive LLM Test Suite
Project: LLM Evaluation Tester (Project 1)
Author: Ankur Sharma

20 test cases across 6 categories:
    1. Factual Accuracy      (4 tests)
    2. Format Compliance     (4 tests)
    3. Hallucination         (4 tests)
    4. Tone & Style          (3 tests)
    5. Instruction Following (3 tests)
    6. Edge Cases            (2 tests)
"""

TEST_CASES = [

    # ─────────────────────────────────────────────
    # CATEGORY 1: FACTUAL ACCURACY (4 tests)
    # Can the model get basic facts right?
    # ─────────────────────────────────────────────

    {
        "id": "test_001",
        "name": "Factual Accuracy - Simple Math",
        "category": "accuracy",
        "system_prompt": "You are a helpful assistant.",
        "user_prompt": "What is 15 + 27?",
        "expected_behavior": "Should return 42 without unnecessary explanation"
    },
    {
        "id": "test_002",
        "name": "Factual Accuracy - World Capital",
        "category": "accuracy",
        "system_prompt": "You are a geography expert.",
        "user_prompt": "What is the capital of Japan?",
        "expected_behavior": "Should answer Tokyo clearly and correctly"
    },
    {
        "id": "test_003",
        "name": "Factual Accuracy - Historical Date",
        "category": "accuracy",
        "system_prompt": "You are a history expert.",
        "user_prompt": "In what year did World War 2 end?",
        "expected_behavior": "Should answer 1945 clearly and correctly"
    },
    {
        "id": "test_004",
        "name": "Factual Accuracy - Science Fact",
        "category": "accuracy",
        "system_prompt": "You are a science teacher.",
        "user_prompt": "What is the chemical formula for water?",
        "expected_behavior": "Should answer H2O clearly and correctly"
    },

    # ─────────────────────────────────────────────
    # CATEGORY 2: FORMAT COMPLIANCE (4 tests)
    # Does the model follow formatting instructions?
    # ─────────────────────────────────────────────

    {
        "id": "test_005",
        "name": "Format Compliance - Haiku",
        "category": "format",
        "system_prompt": "You are a creative poet.",
        "user_prompt": "Write a haiku about artificial intelligence. Follow the 5-7-5 syllable structure exactly.",
        "expected_behavior": "Should be exactly 3 lines with 5-7-5 syllable structure"
    },
    {
        "id": "test_006",
        "name": "Format Compliance - JSON Output",
        "category": "format",
        "system_prompt": "You are a precise assistant who follows instructions exactly.",
        "user_prompt": "Extract the key information and return ONLY valid JSON with keys: name, age, city. Text: 'John is 25 years old and lives in Chicago.'",
        "expected_behavior": "Should return valid JSON only with no extra text or markdown"
    },
    {
        "id": "test_007",
        "name": "Format Compliance - Bullet Points",
        "category": "format",
        "system_prompt": "You are a concise assistant.",
        "user_prompt": "List exactly 3 benefits of exercise. Use bullet points only. No introduction or conclusion.",
        "expected_behavior": "Should return exactly 3 bullet points with no intro or conclusion text"
    },
    {
        "id": "test_008",
        "name": "Format Compliance - Word Limit",
        "category": "format",
        "system_prompt": "You are a concise assistant.",
        "user_prompt": "Explain what machine learning is in exactly 2 sentences. No more, no less.",
        "expected_behavior": "Should return exactly 2 sentences explaining machine learning"
    },

    # ─────────────────────────────────────────────
    # CATEGORY 3: HALLUCINATION DETECTION (4 tests)
    # Does the model make up facts or stay honest?
    # ─────────────────────────────────────────────

    {
        "id": "test_009",
        "name": "Hallucination - Fake Scientist",
        "category": "hallucination",
        "system_prompt": "You are a helpful assistant.",
        "user_prompt": "Tell me about the famous scientist Dr. Zephyr Quantum who invented the flux capacitor in 1955.",
        "expected_behavior": "Should recognize this is fictional and NOT make up information about this person"
    },
    {
        "id": "test_010",
        "name": "Hallucination - Fake Company",
        "category": "hallucination",
        "system_prompt": "You are a business analyst.",
        "user_prompt": "What is the stock price of QuantumLeap Technologies Inc, the AI company founded in 2019?",
        "expected_behavior": "Should say this company doesn't exist or it has no information about it, not make up a stock price"
    },
    {
        "id": "test_011",
        "name": "Hallucination - Future Event",
        "category": "hallucination",
        "system_prompt": "You are a helpful assistant.",
        "user_prompt": "Who won the FIFA World Cup in 2030?",
        "expected_behavior": "Should say it doesn't know since this is a future event, not make up a winner"
    },
    {
        "id": "test_012",
        "name": "Hallucination - Fake Book",
        "category": "hallucination",
        "system_prompt": "You are a literature expert.",
        "user_prompt": "Summarize the novel 'The Quantum Dreams of Captain Zephyr' by J.K. Rowling.",
        "expected_behavior": "Should say this book doesn't exist, not make up a plot summary"
    },

    # ─────────────────────────────────────────────
    # CATEGORY 4: TONE & STYLE (3 tests)
    # Does the model adapt its communication style?
    # ─────────────────────────────────────────────

    {
        "id": "test_013",
        "name": "Tone - ELI5 Explanation",
        "category": "tone",
        "system_prompt": "You are a patient teacher who explains things to 5-year-olds using simple words and fun analogies.",
        "user_prompt": "Explain how a computer works.",
        "expected_behavior": "Should use very simple language, fun analogies, no technical jargon, friendly tone"
    },
    {
        "id": "test_014",
        "name": "Tone - Professional Email",
        "category": "tone",
        "system_prompt": "You are a professional business communication expert.",
        "user_prompt": "Write a professional email requesting a meeting with a client to discuss project updates.",
        "expected_behavior": "Should be formal, professional, include subject line, proper greeting and sign-off"
    },
    {
        "id": "test_015",
        "name": "Tone - Persona Consistency",
        "category": "tone",
        "system_prompt": "You are a pirate. You must speak like a pirate in every response using pirate slang.",
        "user_prompt": "What is the best way to save money?",
        "expected_behavior": "Should answer the question while consistently maintaining pirate persona and slang throughout"
    },

    # ─────────────────────────────────────────────
    # CATEGORY 5: INSTRUCTION FOLLOWING (3 tests)
    # Does the model follow complex instructions?
    # ─────────────────────────────────────────────

    {
        "id": "test_016",
        "name": "Instruction Following - Negative Constraint",
        "category": "instruction",
        "system_prompt": "You are a helpful assistant.",
        "user_prompt": "Describe the ocean without using the words: water, blue, wave, fish, or sea.",
        "expected_behavior": "Should describe the ocean creatively without using any of the 5 forbidden words"
    },
    {
        "id": "test_017",
        "name": "Instruction Following - Multi-step",
        "category": "instruction",
        "system_prompt": "You are a precise assistant.",
        "user_prompt": "Do the following in order: 1) Write a one-word color. 2) Write a one-word animal. 3) Combine them into an adjective-noun phrase.",
        "expected_behavior": "Should follow all 3 steps in order and produce a color + animal phrase"
    },
    {
        "id": "test_018",
        "name": "Instruction Following - Role Reversal",
        "category": "instruction",
        "system_prompt": "You are a helpful assistant.",
        "user_prompt": "Ask me 3 questions about my favorite hobby as if you are interviewing me for a magazine article.",
        "expected_behavior": "Should ask exactly 3 questions in an interview style, not answer them itself"
    },

    # ─────────────────────────────────────────────
    # CATEGORY 6: EDGE CASES (2 tests)
    # How does the model handle unusual inputs?
    # ─────────────────────────────────────────────

    {
        "id": "test_019",
        "name": "Edge Case - Empty Meaning Input",
        "category": "edge_case",
        "system_prompt": "You are a helpful assistant.",
        "user_prompt": "Summarize this text: '   '",
        "expected_behavior": "Should gracefully handle the empty/whitespace input and ask for valid content instead of crashing or making something up"
    },
    {
        "id": "test_020",
        "name": "Edge Case - Contradictory Instructions",
        "category": "edge_case",
        "system_prompt": "You are a helpful assistant.",
        "user_prompt": "Answer this question but do not answer this question: What is 2 + 2?",
        "expected_behavior": "Should recognize the contradiction and handle it gracefully, either by explaining the conflict or making a reasonable choice"
    },

]
