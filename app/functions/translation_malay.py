import openai
from pydantic import BaseModel
from app.utils.ai_functions import AIFunctions
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class TranslateInput(BaseModel):
    text: str
    max_tokens: int = 100

class TranslateOutput(BaseModel):
    translated_text: str

def translate_to_malay(data: TranslateInput) -> TranslateOutput:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Translate the following text to Malay: {data.text}"}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100,
            temperature=0.7,
        )
        translated_text = response["choices"][0]["message"]["content"].strip()
        return TranslateOutput(translated_text=translated_text)
    except Exception as e:
        raise ValueError(f"Failed to translate: {e}")


AIFunctions.register("translate_malay", TranslateInput, TranslateOutput, translate_to_malay)

