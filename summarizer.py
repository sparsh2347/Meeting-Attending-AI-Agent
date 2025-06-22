import openai
from dotenv import load_dotenv
import os

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Set Azure OpenAI configuration
openai.api_type = "azure"
openai.api_base = "https://mindcraft-kapidhwaj-openai-api-key.openai.azure.com/"
openai.api_version = "2024-12-01-preview"

#Here use your openai key (generally load it into .env file for better safety)
openai.api_key = os.getenv("AZURE_OPENAI_KEY")

# ✅ Deployment name from your Azure OpenAI resource
deployment_name = "mindcraft-gpt4o"

#function which takes the meeting transcript as input and summarizes the minutes of meeting and gives action items discussed in the meeting
def summarize_meeting(transcript):
    #prompts for the llm as sytem and user
    """
    Uses Azure OpenAI (GPT-4o) to generate a structured summary of a meeting transcript.

    Args:
        transcript (str): Raw transcript text from a meeting

    Returns:
        str: Structured summary with abstract, key points, and action items
    """

    # ✅ System prompt defines how GPT should behave
    system_msg = {
        "role": "system",
        "content": (
            "You are a meeting assistant AI that reads raw transcripts and outputs "
            "a professional summary including key decisions and action items."
        )
    }

    # ✅ User prompt provides the transcript and output format instructions
    user_msg = {
        "role": "user",
        "content": f"""Summarize the following meeting transcript:
        
{transcript}

Your output format should be:
1. **Abstract Summary:** A brief paragraph.
2. **Key Points:** Bullet-point key decisions or updates.
3. **Preliminary Action Items:** If mentioned, who is doing what (optional)."""
    }

    # ✅ Call Azure-hosted GPT model to get the summary
    response = openai.ChatCompletion.create(
        engine=deployment_name,
        messages=[system_msg, user_msg],
        temperature=0.5,
        max_tokens=800
    )

    #from the list of responses if present provides with the first choice
    return response['choices'][0]['message']['content']

