# outreach/services/prospeo_service.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class ProspeoService:

    API_KEY = os.getenv("PROSPEO_API_KEY")
    BASE_URL = "https://api.prospeo.io"

    @classmethod
    def enrich_person(cls, full_name, company_domain):
        """
        Enrich a person and return verified email details.
        """

        url = f"{cls.BASE_URL}/enrich-person"

        headers = {
            "X-KEY": cls.API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "only_verified_email": True,
            "enrich_mobile": False,
            "data": {
                "full_name": full_name,
                "company_website": company_domain
            }
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=15
            )

            response.raise_for_status()

            return {
                "success": True,
                "data": response.json()
            }

        except requests.exceptions.HTTPError:
            return {
                "success": False,
                "error": response.text
            }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }

    @classmethod
    def enrich_company(cls, company_domain):
        """
        Enrich company information.
        """

        url = f"{cls.BASE_URL}/enrich-company"

        headers = {
            "X-KEY": cls.API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "data": {
                "company_website": company_domain
            }
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=15
            )

            response.raise_for_status()

            return {
                "success": True,
                "data": response.json()
            }

        except requests.exceptions.HTTPError:
            return {
                "success": False,
                "error": response.text
            }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }
        
        # outreach/services/prospeo_service.py

    @classmethod
    def search_people(cls, company_domain):

        url = f"{cls.BASE_URL}/search-person"

        headers = {
            "X-KEY": cls.API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "page": 1,
            "filters": {
                "company": {
                    "websites": {
                        "include": [
                            company_domain
                        ]
                    }
                },
                "person_seniority": {
                    "include": [
                        "C-Suite",
                        "Founder/Owner",
                        # "VP"
                    ]
                }
            }
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=15
        )

        return response.json()

    @classmethod
    def enrich_person_by_id(cls, person_id):

        url = f"{cls.BASE_URL}/enrich-person"

        headers = {
            "X-KEY": cls.API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "only_verified_email": True,
            "data": {
                "person_id": person_id
            }
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=15
        )

        return response.json()