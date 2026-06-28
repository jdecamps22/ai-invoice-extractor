from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


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
You extract structured information from business documents.

Return:
1. Summary
2. Key points
3. Important fields

Be concise and accurate.
"""
            },
            {
                "role": "user",
                "content": request.text
            }
        ]
    )

    return {
        "result": response.choices[0].message.content
    }