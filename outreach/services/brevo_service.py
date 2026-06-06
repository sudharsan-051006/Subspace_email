# outreach/services/brevo_service.py
import os
import requests

class BrevoService:

    API_KEY = os.getenv("BREVO_API_KEY")

    @classmethod
    def send_email(cls, recipient_email, recipient_name):

        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "accept": "application/json",
            "api-key": cls.API_KEY,
            "content-type": "application/json"
        }

        payload = {
            "sender": {
                "name": "AI Outreach Agent",
                "email": "outreach@elinity.in"
            },
            "to": [
                {
                    "email": recipient_email,
                    "name": recipient_name
                }
            ],
            "subject": "Partnership Opportunity",
            "htmlContent": f"""
            <h3>Hello {recipient_name},</h3>

            <p>
            We help companies automate lead generation
            and outreach workflows.
            </p>

            <p>
            Would love to connect.
            </p>
            """
        }

        return requests.post(
            url,
            headers=headers,
            json=payload
        ).json()