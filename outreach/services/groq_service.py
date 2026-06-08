import os
import json
from groq import Groq


class GroqService:

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    @classmethod
    def generate_email(
        cls,
        recipient_name,
        company_name,
        idea
    ):

        prompt = f"""
You are an expert B2B cold email copywriter.

Generate a personalized outreach email.

Recipient Name:
{recipient_name}

Company:
{company_name}

Idea:
{idea}

Return ONLY valid JSON.

Format:

{{
    "subject": "email subject",
    "body": "<html email body>"
}}

Rules:

- Subject should be short and compelling.
- Personalize using recipient name and company name.
- Body must use HTML tags:
  <p>, <br>, <ul>, <li>, <strong>
- Keep email under 200 words.
- Professional tone.
- Include a clear CTA.
- Do NOT wrap JSON inside markdown.
- Do NOT return explanations.
"""

        try:

            response = cls.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7
            )

            content = (
                response
                .choices[0]
                .message
                .content
                .strip()
            )

            try:

                parsed = json.loads(content)

                return {
                    "subject": parsed.get(
                        "subject",
                        "Partnership Opportunity"
                    ),
                    "body": parsed.get(
                        "body",
                        "<p>Hello</p>"
                    )
                }

            except json.JSONDecodeError:

                return {
                    "subject": "Partnership Opportunity",
                    "body": content
                }

        except Exception as e:

            return {
                "subject": "Partnership Opportunity",
                "body": f"<p>Error: {str(e)}</p>"
            }
