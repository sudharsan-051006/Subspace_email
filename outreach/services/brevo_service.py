# outreach/services/brevo_service.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class BrevoService:

    API_KEY = os.getenv("BREVO_API_KEY")
    BASE_URL = "https://api.brevo.com/v3/smtp/email"

    @classmethod
    def send_email(
        cls,
        recipient_email,
        recipient_name,
        subject="Partnership Opportunity",
        html_content=None
    ):

        if not cls.API_KEY:
            return {
                "success": False,
                "error": "BREVO_API_KEY not found in .env"
            }

        headers = {
            "accept": "application/json",
            "api-key": cls.API_KEY,
            "content-type": "application/json"
        }

        if html_content is None:
            html_content = f"""
            <h3>Hello {recipient_name},</h3>

            <p>
            We help companies automate lead generation,
            prospect discovery and outreach workflows.
            </p>

            <p>
            I'd love to explore whether this could be valuable
            for your team.
            </p>

            <p>
            Looking forward to connecting.
            </p>

            <br>

            <p>
            Regards,<br>
            AI Outreach Agent
            </p>
            """

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
            "subject": subject,
            "htmlContent": html_content
        }

        try:

            response = requests.post(
                cls.BASE_URL,
                headers=headers,
                json=payload,
                timeout=30
            )

            print("\n========== BREVO RESPONSE ==========")
            print("Status Code:", response.status_code)
            print("Response Body:", response.text)
            print("====================================\n")

            try:
                response_json = response.json()
            except Exception:
                response_json = {
                    "raw_response": response.text
                }

            if response.status_code in [200, 201]:

                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": response_json
                }

            return {
                "success": False,
                "status_code": response.status_code,
                "error": response_json
            }

        except requests.exceptions.RequestException as e:

            return {
                "success": False,
                "error": str(e)
            }