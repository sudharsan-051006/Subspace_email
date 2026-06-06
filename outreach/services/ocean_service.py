import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OCEAN_API_KEY")

class OceanService:

    @staticmethod
    def get_lookalike_companies(domain):

        response = requests.post(
            "https://api.ocean.io/v3/search/companies",
            headers={
                "X-Api-Token": API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "size": 10,
                "companiesFilters": {
                    "lookalikeDomains": [domain]
                }
            }
        )

        return response.json()