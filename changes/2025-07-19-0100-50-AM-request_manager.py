from fastapi import APIRouter, Depends, HTTPException, Request, Body
from pydantic import BaseModel
from ..utils import authenticate_and_get_user_details
from ..ai_generator.utils import main
from firebase_admin import firestore
from ..firebase_config import db
import json

class QuestionInput(BaseModel):
    question: str

router = APIRouter()

@router.get("/test")
async def test():
    return {"status": "working"}


@router.post('/generate-answer')
async def generate_answer(
    input: QuestionInput = Body(...),  # 👈 Ensure FastAPI parses JSON body
    request_obj: Request = None        # Optional, only if you need headers etc
):
    query = input.question.strip()

    print(query)

    if not query:
        raise HTTPException(status_code=400, detail="Empty question is not allowed.")

    try:
        # Uncomment if auth is needed
        # user_details = authenticate_and_get_user_details(request_obj)
        # user_id = user_details.get('user_id')

        result = await main(query)

        if result["status"] == "INVALID":
            print(result["explanation"])
            return {
                "status": "INVALID",
                "message": result["explanation"]
            }
        
        print(result["response"])

        return {
            "status": "VALID",
            "answer": result["response"],
            "sources": result["ranked_results"]
... (truncated for brevity)