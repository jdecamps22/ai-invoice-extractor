from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# CORS FIX (Vercel + local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class StudyRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {
        "status": "AI Invoice Extractor running"
    }


@app.post("/process-document")
def process_document(request: StudyRequest):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are an AI assistant that extracts structured insights from documents.

Return:
1. Summary
2. Key points
3. Important details
4. Insights

Be clear and structured.
"""
            },
            {
                "role": "user",
                "content": request.text
            }
        ]
    )

    return {
        "success": True,
        "result": response.choices[0].message.content
    }