from dataclasses import dataclass
from groq import AsyncGroq, RateLimitError
import os
from dotenv import load_dotenv
import asyncio
import re

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")

client = AsyncGroq(api_key=api_key)


@dataclass
class MessageResponse:
    response_text: str
    confidence: float
    suggested_action: str
    channel_formatted_response: str
    error: str | None


async def call_api(system_prompt, customer_message):
    response = await asyncio.wait_for(
        client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": customer_message}
            ],
            max_tokens=500
        ),
        timeout=10
    )
    return response.choices[0].message.content


def parse_ai_output(text):
    """Parse structured output from the model."""
    response_match = re.search(r"Response:\s*(.*)", text)
    confidence_match = re.search(r"Confidence:\s*([0-9.]+)", text)
    action_match = re.search(r"SuggestedAction:\s*(\w+)", text)

    response_text = response_match.group(1).strip() if response_match else text.strip()

    try:
        confidence = float(confidence_match.group(1)) if confidence_match else 0.5
    except:
        confidence = 0.5

    suggested_action = action_match.group(1).lower() if action_match else "resolve"

    return response_text, confidence, suggested_action


def format_for_channel(text, channel):
    if channel == "voice":
        sentences = text.split(".")
        return ".".join(sentences[:2]).strip()
    return text


async def handle_message(customer_message, customer_id, channel):

    if not customer_message or not customer_message.strip():
        return MessageResponse(
            response_text="",
            confidence=0.0,
            suggested_action="none",
            channel_formatted_response="",
            error="Empty Input"
        )

    base_prompt = f"""
You are a telecom support agent for MMITS.

Customer ID: {customer_id} is always the same format

You assist with billing issues, service outages, plan changes, and cancellations.
Be professional, empathetic, and accurate.

Never invent account information.
If the issue cannot be resolved safely, recommend escalation.

You must respond in the following format exactly:

Response: <message to customer>
Confidence: <number between 0 and 1>
SuggestedAction: <resolve or escalate>
"""

    if channel == "voice":
        channel_instruction = """
The customer is speaking on a phone call.
Keep the Response under 2 sentences.
No bullet points or formatting.
"""
    elif channel == "whatsapp":
        channel_instruction = """
Respond in short conversational lines suitable for WhatsApp.
Avoid long paragraphs.
"""
    else:
        channel_instruction = """
Respond clearly and thoroughly as this is live chat.
"""

    system_prompt = base_prompt + channel_instruction

    try:
        raw_text = await call_api(system_prompt, customer_message)

        response_text, confidence, suggested_action = parse_ai_output(raw_text)

        formatted = format_for_channel(response_text, channel)

        return MessageResponse(
            response_text=response_text,
            confidence=confidence,
            suggested_action=suggested_action,
            channel_formatted_response=formatted,
            error=None
        )

    except asyncio.TimeoutError:
        return MessageResponse(
            response_text="",
            confidence=0.0,
            suggested_action="escalate",
            channel_formatted_response="",
            error="Request timed out after 10 seconds"
        )

    except RateLimitError:
        await asyncio.sleep(2)
        try:
            raw_text = await call_api(system_prompt, customer_message)

            response_text, confidence, suggested_action = parse_ai_output(raw_text)

            formatted = format_for_channel(response_text, channel)

            return MessageResponse(
                response_text=response_text,
                confidence=confidence,
                suggested_action=suggested_action,
                channel_formatted_response=formatted,
                error=None
            )

        except Exception as e:
            return MessageResponse(
                response_text="",
                confidence=0.0,
                suggested_action="escalate",
                channel_formatted_response="",
                error=f"Rate limit retry failed: {str(e)}"
            )

    except Exception as e:
        return MessageResponse(
            response_text="",
            confidence=0.0,
            suggested_action="escalate",
            channel_formatted_response="",
            error=str(e)
        )


if __name__ == "__main__":

    result = asyncio.run(handle_message("my bill is wrong", "cust_001", "chat"))
    print(result)

    result = asyncio.run(handle_message("   ", "cust_002", "chat"))
    print(result)
