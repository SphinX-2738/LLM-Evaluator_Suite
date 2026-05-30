"""
test_runner.py - Run test cases and save results
Purpose: Automate testing of LLM responses
Author: Ankur
Date: Week 1, Day 2
"""

from groq import Groq
from test_cases import TEST_CASES
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY")) # Replace with your key

# Configuration
MODEL = "llama-3.3-70b-versatile"
TEMPERATURE = 0.7
MAX_TOKENS = 300

# Create results directory if it doesn't exist
os.makedirs("test_results", exist_ok=True)

def run_single_test(test_case):
    """
    Run a single test case and return results
    
    Args:
        test_case (dict): Test case with prompt and metadata
        
    Returns:
        dict: Test results including response and token usage
    """
    print(f"\n{'='*60}")
    print(f"Running: {test_case['name']}")
    print(f"ID: {test_case['id']}")
    print(f"Category: {test_case['category']}")
    print('='*60)
    
    try:
        # Make API call
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": test_case['system_prompt']},
                {"role": "user", "content": test_case['user_prompt']}
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        
        # Extract response
        ai_response = response.choices[0].message.content
        
        # Get token usage
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        
        # Print response preview
        print(f"\n✅ Test completed successfully")
        print(f"Response preview: {ai_response[:100]}...")
        print(f"Tokens used: {total_tokens} (prompt: {prompt_tokens}, completion: {completion_tokens})")
        
        # Prepare result
        result = {
            "test_id": test_case['id'],
            "test_name": test_case['name'],
            "category": test_case['category'],
            "timestamp": datetime.now().isoformat(),
            "system_prompt": test_case['system_prompt'],
            "user_prompt": test_case['user_prompt'],
            "expected_behavior": test_case['expected_behavior'],
            "ai_response": ai_response,
            "model": MODEL,
            "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS,
            "token_usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens
            },
            "status": "success"
        }
        
        return result
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        
        result = {
            "test_id": test_case['id'],
            "test_name": test_case['name'],
            "category": test_case['category'],
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "status": "failed"
        }
        
        return result

def run_all_tests():
    """
    Run all test cases and save results
    """
    print("\n" + "="*60)
    print("🚀 STARTING TEST RUN")
    print("="*60)
    print(f"Total tests: {len(TEST_CASES)}")
    print(f"Model: {MODEL}")
    print(f"Temperature: {TEMPERATURE}")
    print(f"Max tokens: {MAX_TOKENS}")
    
    all_results = []
    total_tokens = 0
    successful_tests = 0
    failed_tests = 0
    
    # Run each test
    for test_case in TEST_CASES:
        result = run_single_test(test_case)
        all_results.append(result)
        
        if result['status'] == 'success':
            successful_tests += 1
            total_tokens += result['token_usage']['total_tokens']
        else:
            failed_tests += 1
    
    # Calculate cost (Groq is free, but let's calculate as if it was OpenAI for practice)
    # OpenAI GPT-4o-mini pricing: $0.150 per 1M input tokens, $0.600 per 1M output tokens
    estimated_cost = (total_tokens / 1_000_000) * 0.15  # Simplified calculation
    
    # Create summary
    summary = {
        "run_timestamp": datetime.now().isoformat(),
        "total_tests": len(TEST_CASES),
        "successful_tests": successful_tests,
        "failed_tests": failed_tests,
        "total_tokens_used": total_tokens,
        "estimated_cost_usd": round(estimated_cost, 4),
        "model": MODEL,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS
    }
    
    # Save results to JSON file
    output_filename = f"test_results/test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    output_data = {
        "summary": summary,
        "results": all_results
    }
    
    with open(output_filename, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    # Print summary
    print("\n" + "="*60)
    print("📊 TEST RUN SUMMARY")
    print("="*60)
    print(f"✅ Successful: {successful_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"🔢 Total tokens: {total_tokens}")
    print(f"💰 Estimated cost: ${estimated_cost:.4f}")
    print(f"💾 Results saved to: {output_filename}")
    print("="*60)
    
    return output_data

if __name__ == "__main__":
    results = run_all_tests()