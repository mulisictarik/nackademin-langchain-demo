# 🤖 AI Agents Project

> A collection of intelligent, conversational AI agents built with **LangChain**, **LangGraph** and **Ollama** — each with a unique personality, purpose and set of tools.

---

## ✨ Agents

### 📚 Agent 1 — Study Assistant (Professor Hoof)

> _"Learning made simple, one concept at a time."_

Professor Hoof is a patient and experienced study coach who breaks down complex topics into simple explanations. He creates quizzes, flashcards and personalized study plans to help you master any subject.

**Tools:**

- `create_quiz` — Generates quiz questions on any topic
- `make_flashcard` — Creates flashcards for memorization
- `suggest_study_plan` — Builds a personalized study schedule

---

### 🍳 Agent 2 — Culinary Expert (Chef Mulisic)

> _"Transforming everyday ingredients into culinary masterpieces."_

Chef Mulisic is a creative and passionate master chef. Whether you need a recipe based on what's in your fridge, want to find a smart ingredient substitute, or need the perfect wine pairing, Chef Mulisic is your guide in the kitchen.

**Tools:**

- `generate_recipe` — Creates a recipe from a list of ingredients
- `substitute_ingredient` — Finds alternatives for missing ingredients
- `pair_wine` — Suggests the perfect wine for a specific dish

---

### 💼 Agent 3 — Career Advisor (CV Pro)

> _"Elevating your career, one application at a time."_

CV Pro is a sharp and professional career advisor. By analyzing your online resume links and understanding your target role, CV Pro helps you stand out in the job market with actionable feedback and tailored cover letters.

**Tools:**

- `analyze_cv_link` — Extracts and reviews content from a CV/LinkedIn URL
- `suggest_improvements` — Gives actionable feedback based on target roles
- `generate_cover_letter` — Drafts a professional cover letter for a specific job

---

## 🛠️ Tech Stack

| Technology              | Purpose               |
| ----------------------- | --------------------- |
| 🐍 Python 3             | Core language         |
| 🦜 LangChain            | Agent framework       |
| 🕸️ LangGraph            | Agent execution graph |
| 🦙 Ollama (llama3.1:8b) | Local LLM backend     |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/mulisictarik/nackademin-langchain-demo.git
cd nackademin-langchain-demo
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows
```

### 3. Install dependencies

```bash
pip install langchain langchain-ollama langgraph python-dotenv
```

### 4. Create your `.env` file

```bash
OLLAMA_BASE_URL=your-ollama-server-url
OLLAMA_BEARER_TOKEN=your-token-here
```

## ▶️ Running the Agents

```bash
# Study Assistant
python -m agents.study_agent.study_agent

# Culinary Expert
python -m agents.chef_agent.chef_agent

# Career Advisor
python -m agents.cv_agent.cv_agent


## 👨‍💻 Author & Developer

**Tarik Mulisic**
*ML OPS Student @ Nackademin*

```
