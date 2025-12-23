import os
from google import genai
from google.genai import types


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_ai_email(lead):
    prompt = f"""
You are a sales copywriter.

Write a short cold email for a digital marketing agency.

Business Name: {lead.business_name}
Industry: {lead.industry}
City: {lead.city}

Keep it professional, friendly, and under 120 words.
End with a clear call to action.
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-flash-lite-latest",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=300,
            ),
        )
    except Exception as e:
        return fallback_email(lead)

    if not response or not response.text:
        return fallback_email(lead)

    text = response.text.strip()

    # ---------- SAFE PARSING ----------
    subject = f"Helping {lead.business_name} grow"
    body = text

    # Try to extract subject if present
    if "Subject:" in text:
        try:
            subject = text.split("Subject:")[1].split("\n")[0].strip()
            body = text.split("\n", 1)[1].strip()
        except Exception:
            pass

    return {
        "subject": subject,
        "body": body
    }


def fallback_email(lead):
    return {
        "subject": f"Helping {lead.business_name} get more customers",
        "body": f"""Hi,

We help {lead.industry} businesses in {lead.city} attract more customers through digital marketing.

Would you like to explore how this could work for {lead.business_name}?

Best regards,
Your Team"""
    }
