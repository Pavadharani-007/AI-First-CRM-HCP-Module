# backend/tools.py

form_data = {
    "hcp_name": "",
    "date": "",
    "sentiment": "",
    "product": "",
    "brochure": False
}

# ---------------- TOOL 1: LOG INTERACTION ----------------
def log_interaction(data: dict):
    """
    Stores interaction data without overwriting edited values
    """
    for key in form_data:
        if key in data and data[key] not in [None, ""]:
            # only fill empty fields (DO NOT overwrite edited values)
            if form_data[key] in ["", None, False]:
                form_data[key] = data[key]

    return form_data


# ---------------- TOOL 2: EDIT INTERACTION ----------------
def edit_interaction(updates: dict):
    """
    Updates only provided fields safely
    """
    for key, value in updates.items():
        if key in form_data and value not in [None, ""]:
            form_data[key] = value

    return form_data


# ---------------- TOOL 3: SUMMARY ----------------
def summarize_interaction():
    name = form_data.get("hcp_name") or "HCP"
    sentiment = form_data.get("sentiment") or "neutral"
    product = form_data.get("product") or "general topics"

    return f"{name} had a {sentiment} interaction and discussed {product}."


# ---------------- TOOL 4: SENTIMENT ----------------
def sentiment_tool(text: str):
    text = text.lower()

    if "positive" in text:
        form_data["sentiment"] = "positive"
    elif "negative" in text:
        form_data["sentiment"] = "negative"
    else:
        form_data["sentiment"] = "neutral"

    return form_data["sentiment"]


# ---------------- TOOL 5: INSIGHT ----------------
def hcp_insight():
    sentiment = form_data.get("sentiment", "")

    if sentiment == "positive":
        return "High Priority HCP - strong engagement"
    elif sentiment == "negative":
        return "Low Priority HCP - needs follow-up"
    else:
        return "Medium Priority HCP - neutral engagement"