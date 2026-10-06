import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq


app = FastAPI(
    title="AI Memory Palace Backend",
    version="2.0.0"
)


# ---------- CORS ----------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- GROQ CLIENT ----------

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)
else:
    groq_client = None


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
        "status": "healthy",
        "ai_configured": groq_client is not None
    }


# ---------- AI CONCEPT GENERATOR ----------

@app.post("/generate-concepts")
def generate_concepts(request: ConceptRequest):

    topic = request.topic.strip()

    if not topic:
        raise HTTPException(
            status_code=400,
            detail="Topic is required"
        )

    if groq_client is None:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is not configured"
        )

    prompt = f"""
You are the AI learning planner for an immersive VR Memory Palace.

The learner wants to learn this topic:

{topic}

Break the topic into exactly 5 important concepts.

The concepts should:
- be educationally meaningful
- be easy to represent as separate 3D objects
- follow a logical learning order
- help the learner remember the topic
- avoid unnecessary details

Return JSON only in this structure:

{{
  "concepts": [
    {{
      "name": "Concept name",
      "description": "Short explanation",
      "memory_hint": "A memorable visual or spatial idea"
    }}
  ]
}}
"""

    try:

        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You create concise educational concepts "
                        "for an immersive VR memory palace."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={
                "type": "json_object"
            },
            temperature=0.3,
            max_completion_tokens=1200
        )

        content = response.choices[0].message.content

        data = json.loads(content)

        return {
            "status": "success",
            "topic": topic,
            "concepts": data["concepts"]
        }

    except Exception as error:

        print(
            "Concept generation error:",
            str(error)
        )

        raise HTTPException(
            status_code=500,
            detail="AI concept generation failed"
        )
