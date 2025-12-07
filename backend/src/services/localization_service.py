from openai import OpenAI
from ..config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def translate_text(text: str, target_language: str) -> str:
    """
    Translates the given text into the target language using OpenAI.
    """
    
    prompt = f"""
    You are an expert technical translator.
    
    Task:
    Translate the following technical textbook content into {target_language}.
    - Ensure accuracy of technical terms.
    - Maintain the original tone and formatting.
    - If the target is Urdu, use the Urdu script.
    
    Content:
    {text}
    
    Translation:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional translator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3, # Lower temperature for accurate translation
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating translation: {e}")
        return f"Error translating content. Original text: {text}"
