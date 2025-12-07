from openai import OpenAI
from ..config import settings
from ..models import orm

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def personalize_text(text: str, user: orm.Student) -> str:
    """
    Personalizes the given text based on the student's background.
    """
    
    background_info = []
    if user.software_background:
        background_info.append(f"Software Engineering Background: {user.software_background}")
    if user.hardware_background:
        background_info.append(f"Hardware Knowledge: {user.hardware_background}")
    if user.language_preference and user.language_preference != 'en':
        background_info.append(f"Preferred Language: {user.language_preference}")

    context_str = ". ".join(background_info)
    
    if not context_str:
        return "No personalization context available. Here is the original text:\n" + text

    prompt = f"""
    You are an expert AI tutor for Physical AI and Humanoid Robotics.
    
    Student Profile:
    {context_str}
    
    Task:
    Rewrite or Annotate the following textbook content to be more understandable for this specific student.
    - If they know Python, use Python analogies.
    - If they know C++, compare concepts to C++.
    - If they have hardware experience, focus on the physical implementation details.
    - Keep the core meaning identical, just enhance the explanation.
    
    Textbook Content:
    {text}
    
    Personalized Explanation:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Cost-effective for hackathon
            messages=[
                {"role": "system", "content": "You are a helpful and adaptive AI tutor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating personalization: {e}")
        return f"Error creating personalization. Original text: {text}"
