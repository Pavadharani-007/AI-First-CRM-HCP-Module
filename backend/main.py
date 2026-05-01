from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend.agent import run_agent
from backend.tools import edit_interaction   # ✅ added

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- REQUEST MODELS ----------------
class ChatRequest(BaseModel):
    message: str


class EditRequest(BaseModel):
    hcp_name: str = ""
    sentiment: str = ""
    product: str = ""
    brochure: bool = False
    date: str = ""


# ---------------- ROUTES ----------------
@app.get("/")
def home():
    return {"message": "Backend running"}


@app.post("/chat")
def chat(req: ChatRequest):
    result = run_agent(req.message)
    return result


@app.post("/edit")
def edit(req: EditRequest):
    return edit_interaction(req.dict())