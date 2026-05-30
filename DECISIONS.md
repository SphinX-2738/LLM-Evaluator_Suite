# Architectural Decisions

This document explains the key decisions made while building the LLM Evaluator Suite.

---

## 1. Why Groq API?

**Decision:** Use Groq as the LLM provider instead of OpenAI or Anthropic.

**Reasoning:**
- Groq offers extremely fast inference (low latency) which speeds up test runs significantly
- Generous free tier allows experimentation without immediate cost
- API is OpenAI-compatible, making it easy to switch providers later if needed

---

## 2. Why LLM-as-Judge instead of rule-based evaluation?

**Decision:** Use a second LLM call to score outputs rather than regex/keyword matching.

**Reasoning:**
- LLM outputs are open-ended — rule-based checks miss nuance
- An LLM judge can reason about hallucination, relevance, and tone in ways rules cannot
- More scalable: works across different prompt types without rewriting logic
- Tradeoff: adds cost per evaluation (one extra API call per test)

---

## 3. Why separate modules (test_runner, evaluator, report_generator)?

**Decision:** Split functionality into separate files rather than one big script.

**Reasoning:**
- Each module has a single responsibility — easier to debug and extend
- Can run them independently (e.g., regenerate a report without re-running tests)
- Mirrors real-world software engineering practices

---

## 4. Why file-based storage (JSON files) instead of a database?

**Decision:** Save results to JSON files in test_results/ folder.

**Reasoning:**
- No database setup required — reduces friction for getting started
- JSON files are human-readable and easy to inspect
- Sufficient for the scale of this project (tens to hundreds of test runs)
- Tradeoff: doesn't scale well to thousands of runs — a database would be needed then

---

## 5. Why score on Hallucination, Format, and Relevance specifically?

**Decision:** Use these three metrics as the core evaluation dimensions.

**Reasoning:**
- **Hallucination** — the most critical failure mode for LLMs in production
- **Format compliance** — many real-world use cases depend on structured output
- **Relevance** — ensures the model is actually answering what was asked
- Together they cover the three most common ways LLM outputs fail in practice
