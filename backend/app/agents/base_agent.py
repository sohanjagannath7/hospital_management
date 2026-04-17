import google.generativeai as genai
import json
import time
import re
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
MODEL = "gemini-1.5-flash"


def call_gemini(system: str, user_message: str, json_schema: dict) -> tuple[dict, int]:
    """
    Calls Gemini and returns (parsed_json_dict, elapsed_ms).
    Instructs the model to respond only with JSON matching the given schema.
    """
    prompt = (
        f"{system}\n\n"
        f"Respond ONLY with a valid JSON object matching this schema (no markdown, no explanation):\n"
        f"{json.dumps(json_schema, indent=2)}\n\n"
        f"{user_message}"
    )

    start = time.time()
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(prompt)
    elapsed = int((time.time() - start) * 1000)

    text = response.text.strip()
    # Strip markdown code fences if Gemini wraps output
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text), elapsed
    except json.JSONDecodeError:
        # Attempt to extract first JSON object from the text
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group()), elapsed
        return {}, elapsed
