# ---------------- GLOBAL STATE ----------------
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
    Stores extracted interaction data into form state
    """
    for key in form_data:
        if key in data and data[key] is not None:
            form_data[key] = data[key]

    return form_data


# ---------------- TOOL 2: EDIT INTERACTION ----------------
def edit_interaction(updates: dict):
    """
    Updates only specific fields in form data
    """
    for key, value in updates.items():
        if key in form_data:
            form_data[key] = value

    return form_data


# ---------------- TOOL 3: SUMMARIZE ----------------
def summarize_interaction():
    """
    Generates clean interaction summary
    """
    name = form_data.get("hcp_name") or "HCP"
    sentiment = form_data.get("sentiment") or "neutral"
    product = form_data.get("product") or "general topics"

    return f"{name} had a {sentiment} interaction and discussed {product}."


# ---------------- TOOL 4: SENTIMENT ANALYSIS ----------------
def sentiment_tool(text: str):
    """
    Basic sentiment detection (can be replaced by LLM later)
    """
    text = text.lower()

    if "positive" in text:
        form_data["sentiment"] = "positive"
    elif "negative" in text:
        form_data["sentiment"] = "negative"
    else:
        form_data["sentiment"] = "neutral"

    return form_data["sentiment"]


# ---------------- TOOL 5: HCP INSIGHT ----------------
def hcp_insight():
    """
    Generates priority level for HCP
    """
    sentiment = form_data.get("sentiment", "")

    if sentiment == "positive":
        return "High Priority HCP - strong engagement"
    elif sentiment == "negative":
        return "Low Priority HCP - needs follow-up"
    else:
        return "Medium Priority HCP - neutral engagement"