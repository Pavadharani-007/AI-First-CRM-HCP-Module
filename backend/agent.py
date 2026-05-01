from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from typing import TypedDict
from backend.tools import (
    log_interaction,
    edit_interaction,
    summarize_interaction,
    sentiment_tool,
    hcp_insight
)
import os
import json
import re

# ---------------- API KEY ----------------
os.environ["GROQ_API_KEY"] = "your_api_key_here"  # 🔐 replace with your key

llm = ChatGroq(model="llama-3.3-70b-versatile")


# ---------------- STATE ----------------
class State(TypedDict, total=False):
    message: str
    parsed: dict
    form_data: dict
    summary: str
    insight: str
    mode: str   # 🔥 NEW (create/edit)


# ---------------- NODE 1: ANALYZE ----------------
def analyze_node(state):
    message = state.get("message", "")
    msg_lower = message.lower()

    # 🔥 STEP 1: DETECT EDIT VIA CHAT
    if any(word in msg_lower for word in ["change", "update", "edit"]):
        updates = {}

        if "sentiment" in msg_lower:
            if "positive" in msg_lower:
                updates["sentiment"] = "positive"
            elif "negative" in msg_lower:
                updates["sentiment"] = "negative"
            else:
                updates["sentiment"] = "neutral"

        if "product" in msg_lower:
            if "tablet" in msg_lower:
                updates["product"] = "Tablet"

        if "brochure" in msg_lower:
            if "no" in msg_lower:
                updates["brochure"] = False
            else:
                updates["brochure"] = True

        state["parsed"] = updates
        state["mode"] = "edit"
        return state

    # 🔥 STEP 2: NORMAL CREATE FLOW (LLM)
    prompt = f"""
Extract structured data from this message.

Message:
{message}

Return ONLY valid JSON. No explanation.

{{
  "hcp_name": "Dr Smith",
  "sentiment": "positive",
  "brochure": true,
  "product": "Aspirin",
  "date": null
}}

Rules:
- Extract doctor name if present
- sentiment: positive / negative / neutral
- brochure = true if mentioned
- product if mentioned else null
- date = null if not mentioned
"""

    response = llm.invoke(prompt)
    content = response.content.strip()

    print("RAW LLM OUTPUT:", content)

    try:
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
        else:
            raise ValueError("No JSON found")
    except:
        print("JSON PARSE FAILED")
        parsed = {
            "hcp_name": "",
            "sentiment": "neutral",
            "brochure": False,
            "product": "",
            "date": None
        }

    state["parsed"] = parsed
    state["mode"] = "create"
    return state


# ---------------- NODE 2: LOG / EDIT ----------------
def log_node(state):
    data = state.get("parsed", {})

    # 🔥 SWITCH TOOL BASED ON MODE
    if state.get("mode") == "edit":
        state["form_data"] = edit_interaction(data)
    else:
        state["form_data"] = log_interaction(data)

    return state


# ---------------- NODE 3: SENTIMENT ----------------
def edit_node(state):
    message = state.get("message", "")
    state["sentiment"] = sentiment_tool(message)
    return state


# ---------------- NODE 4: SUMMARY ----------------
def summary_node(state):
    state["summary"] = summarize_interaction()
    return state


# ---------------- NODE 5: INSIGHT ----------------
def insight_node(state):
    state["insight"] = hcp_insight()
    return state


# ---------------- GRAPH ----------------
graph = StateGraph(State)

graph.add_node("analyze", analyze_node)
graph.add_node("log", log_node)
graph.add_node("edit", edit_node)
graph.add_node("summary", summary_node)
graph.add_node("insight", insight_node)

graph.set_entry_point("analyze")

graph.add_edge("analyze", "log")
graph.add_edge("log", "edit")
graph.add_edge("edit", "summary")
graph.add_edge("summary", "insight")
graph.add_edge("insight", END)

app = graph.compile()


# ---------------- FINAL OUTPUT ----------------
def run_agent(message: str):
    result = app.invoke({"message": message})

    print("FINAL RESULT:", result)

    return {
        "form_data": result.get("form_data", {}),
        "summary": result.get("summary", ""),
        "insight": result.get("insight", "")
    }