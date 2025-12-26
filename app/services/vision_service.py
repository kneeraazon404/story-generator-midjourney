import base64
import json
import logging
import os

import dotenv
import openai
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load API key
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

SYSTEM_PROMPT = """You are a warm, empathetic, and creative personal biographer and storyteller.
Your task is to look at a user-uploaded photo and write a short, personalized narrative story about it.
You will be properly provided with metadata: Name(s), Date, and a Short Note.
Incorporate these details naturally into the narrative.
Do NOT simply describe the visual elements (e.g., "I see a person standing..."). Instead, weave a story *surrounding* that moment.
Focus on emotions, atmosphere, and the significance of the memory.
The tone should be nostalgic, celebratory, or reflective, depending on the image content.
Output strictly JSON: {"title": "Creative Title", "story": "The narrative text..."}
"""


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def generate_story_from_image(image_path, metadata):
    """
    Analyzes an image and generates a narrative story using GPT-4o.
    """
    try:
        base64_image = encode_image(image_path)

        name = metadata.get("name", "Someone special")
        date = metadata.get("date", "Use context cues")
        note = metadata.get("note", "")

        user_content = f"""
        Here is a photo.
        Metadata provided by user:
        - People/Subject Name: {name}
        - Date/Time: {date}
        - User's Note: {note}

        Write a short narrative story (approx 150-200 words) capturing this moment.
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_content},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                },
            ],
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        content = response.choices[0].message.content
        logging.info(f"Vision Story Response: {content}")

        if content:
            # Basic cleanup
            cleaned = content.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)
        return {"title": "Error", "story": "Could not generate story."}

    except Exception as e:
        logging.error(f"Error in vision story generation: {e}")
        return {
            "title": "Error",
            "story": "An error occurred while analyzing the image.",
        }
