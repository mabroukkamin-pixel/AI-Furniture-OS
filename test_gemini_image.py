from google import genai
from runtime.config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)

client = genai.Client(
    api_key=GEMINI_API_KEY
)

print("Testing Gemini...")
print("Model:", GEMINI_MODEL)

response = client.models.generate_content(
    model=GEMINI_MODEL,
    contents="Say only: Gemini is working"
)

print(response.text)