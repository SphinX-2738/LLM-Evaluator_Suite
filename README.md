# 🧪 LLM Evaluator Suite

A production-grade evaluation framework for Large Language Models — built to test, score, and report on LLM outputs using automated LLM-as-judge methodology.

---

## 🚀 What This Does

Most developers just *hope* their LLM outputs are correct. This suite **measures** them.

Given a set of test prompts, it:
1. Sends each prompt to an LLM via API
2. Evaluates the response using a second LLM-as-judge call
3. Scores each response on **hallucination**, **format compliance**, and **relevance**
4. Generates structured reports with pass/fail status, cost tracking, and timestamps

---

## 📁 Project Structure

```
llm-evaluator-suite/
│
├── first_call.py           # Initial API connection test
├── temperature_test.py     # Experiments with temperature parameter
├── system_prompt_test.py   # Experiments with system prompt variations
├── test_cases.py           # Defined test cases (inputs + expectations)
├── test_runner.py          # Runs all test cases through the LLM
├── evaluator.py            # LLM-as-judge scoring logic
├── report_generator.py     # Generates final evaluation reports
│
├── reports/                # Generated HTML/JSON reports (gitignored)
├── test_results/           # Raw LLM outputs saved per run (gitignored)
│
├── .env                    # API keys — never committed
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🧠 Core Concepts Demonstrated

- **LLM-as-Judge Pattern** — Using a second LLM call to evaluate the first
- **Structured Evaluation** — Scoring on hallucination, format compliance, and relevance (0–10)
- **Parameter Experimentation** — Documented effects of temperature and system prompts
- **Cost Tracking** — Token usage and estimated cost logged per test run
- **Automated Reporting** — Human-readable reports generated per evaluation run

---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/SphinX-2738/llm-evaluator-suite.git
cd llm-evaluator-suite
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Usage

### Run the full evaluation pipeline
```bash
python test_runner.py
```

### Generate a report from results
```bash
python report_generator.py
```

---

## 📊 Sample Report Output

| Test Name         | Hallucination | Format | Relevance | Status | Cost     |
|-------------------|---------------|--------|-----------|--------|----------|
| Factual QA        | 9/10          | 10/10  | 9/10      | ✅ Pass | $0.0004 |
| Format Compliance | 8/10          | 9/10   | 10/10     | ✅ Pass | $0.0003 |
| Edge Case Input   | 6/10          | 7/10   | 8/10      | ⚠️ Review | $0.0005 |

---

## 🔑 Key Design Decisions

See [`DECISIONS.md`](./DECISIONS.md) for full architectural reasoning. Summary:

- **Groq API** chosen for fast inference and generous free tier
- **LLM-as-judge** chosen over rule-based evaluation for flexibility with open-ended outputs
- **Separate evaluator module** keeps scoring logic decoupled from test running
- **JSON + file-based storage** for simplicity — no database needed at this scale

---

## 📈 What I Learned

- How to structure HTTP requests to LLM APIs and handle responses
- How temperature affects output variability in practice
- How to design meaningful test cases covering factual, format, and edge case scenarios
- How to use AI to evaluate AI outputs reliably
- Cost tracking and token management at scale

---

## 🛣️ What's Next

This is **Project 1 of 3** in my Generative AI Engineering portfolio:

- ✅ **Project 1** — LLM Evaluator Suite *(this repo)*
- 🔄 **Project 2** — Structured Data Extractor *(in progress)*
- ⏳ **Project 3** — Multi-Stage Content Pipeline

---

## 🧑‍💻 Author

**Ankur**
Building a portfolio in Generative AI Engineering — one project at a time.

- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Ankur Sharma](https://www.linkedin.com/in/ankur-sharma-37a0a3276/)
