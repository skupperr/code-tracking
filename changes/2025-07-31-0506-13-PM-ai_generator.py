import os
import json
import requests
from typing import Dict, Any

OLLAMA_MODEL = "gemma3"  # Use the name of your local Ollama model

def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    system_prompt = """You are an expert coding challenge creator.
Your task is to generate a coding question with multiple choice answers.
The question should be appropriate for the specified difficulty level.

For easy questions: Focus on basic syntax, simple operations, or common programming concepts.
For medium questions: Cover intermediate concepts like data structures, algorithms, or language features.
For hard questions: Include advanced topics, design patterns, optimization techniques, or complex algorithms.

Return ONLY the challenge in valid raw JSON format, like this:
{
    "title": "The question title",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "correct_answer_id": 0,
    "explanation": "Detailed explanation of why the correct answer is right"
}

Do NOT include any markdown, code fences, or additional explanation outside the JSON.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate a {difficulty} difficulty coding challenge."}
                ],
                "temperature": 0.7,
                "stream": False
            }
        )
        response.raise_for_status()

        content = response.json().get("message", {}).get("content", "").strip()

        print("Content: ", content)

        # Strip code block if present
        if content.startswith("