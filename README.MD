# 🤖 AI-First CRM HCP Module

## 📌 Project Overview
This project is an AI-first CRM system designed for Healthcare Professionals (HCP) interaction logging.  
It allows users to log interactions via a chat-based AI assistant, which automatically extracts structured data and updates a form in real time.

The system is built using LangGraph for AI workflow orchestration and FastAPI for backend APIs.

---

## 🚀 Features

- Chat-based interaction logging
- Automatic extraction of HCP details (name, sentiment, product, brochure)
- AI-powered summarization of interactions
- HCP insight generation (priority level)
- Edit interaction via chat commands
- Real-time form update from AI responses

---

## 🧠 AI Architecture

- LangGraph is used to manage multi-step AI workflow:
  1. Analyze user input (LLM extraction)
  2. Log interaction (tool)
  3. Edit interaction (tool)
  4. Generate summary
  5. Generate HCP insight

- LLM used: `llama-3.3-70b-versatile` (Groq API)

---

## 🛠 Tech Stack

### Frontend:
- React.js
- JavaScript
- CSS

### Backend:
- FastAPI
- Python
- LangGraph
- LangChain Groq

---

## 📂 Project Structure
