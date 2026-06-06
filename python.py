from outreach.services.prospeo_service import ProspeoService

result = ProspeoService.search_people(
    "intercom.com"
)

print(result)