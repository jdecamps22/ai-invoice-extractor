from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import json

app = FastAPI()

# CORS (needed for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI()


class DocumentRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {"status": "AI Invoice Extractor running"}


@app.post("/process-document")
def process_document(request: DocumentRequest):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are an AI that extracts structured data from invoices and business documents.

Return ONLY valid JSON in this format:

{
  "summary": "short description of the invoice",
  "invoice_number": "",
  "client_name": "",
  "total_amount": "",
  "due_date": "",
  "items": ["item1", "item2"],
  "key_points": ["important details"]
}

Rules:
- Output ONLY JSON
- No explanations
- No markdown
- If missing, use ""
"""
            },
            {
                "role": "user",
                "content": request.text
            }
        ]
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {
            "error": "Invalid JSON from model",
            "raw_output": content
        }