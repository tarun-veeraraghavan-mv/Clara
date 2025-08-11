from langchain.tools import tool
from ..utils.llm import llm

@tool
def analyze_image(image_url: str, user_input: str) -> str:
    """
    Analyzes an image from a URL and provides a summary of its features based on the user's input.
    """
    res = llm.invoke([
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_input},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        }
    ])
    return res.content
