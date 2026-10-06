from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(
    title="AI Memory Palace Backend",
    version="1.1.0"
)


# Allow the VR frontend to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- MODELS ----------

class ConceptRequest(BaseModel):
    topic: str


# ---------- ROOT ----------

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "AI Memory Palace Backend is running"
    }


# ---------- HEALTH ----------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ---------- AI CONCEPT GENERATOR ----------

@app.post("/generate-concepts")
def generate_concepts(request: ConceptRequest):

    topic = request.topic.strip()

    if not topic:
        return {
            "status": "error",
            "message": "Topic is required"
        }

    # Temporary concept generation.
    # The LLM will be connected in the next step.
    concepts = [
        {
            "name": f"{topic} - Core Idea",
            "description": f"The central idea of {topic}."
        },
        {
            "name": f"{topic} - Key Concept 1",
            "description": f"An important concept related to {topic}."
        },
        {
            "name": f"{topic} - Key Concept 2",
            "description": f"Another important concept related to {topic}."
        },
        {
            "name": f"{topic} - Process",
            "description": f"The main process or mechanism involved in {topic}."
        },
        {
            "name": f"{topic} - Application",
            "description": f"A practical application of {topic}."
        }
    ]

    return {
        "status": "success",
        "topic": topic,
        "concepts": concepts
    }
