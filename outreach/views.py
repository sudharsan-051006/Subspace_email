from django.shortcuts import render
from .services.ocean_service import OceanService
from .services.prospeo_service import ProspeoService


def home(request):

    results = []

    if request.method == "POST":

        domain = request.POST.get("domain")

        ocean_result = OceanService.get_lookalike_companies(domain)

        companies = ocean_result.get("companies", [])[:5]

        for company in companies:

            company_data = company.get("company", {})

            company_domain = company_data.get("domain")

            if not company_domain:
                continue

            people_result = ProspeoService.search_people(
                company_domain
            )

            decision_makers = []

            for person_data in people_result.get("results", []):

                person = person_data.get("person", {})

                title = person.get(
                    "current_job_title",
                    ""
                ).lower()

                if any(keyword in title for keyword in [
                    "ceo",
                    "founder",
                    "chief",
                    "cto",
                    "cfo",
                    "cmo",
                    "coo",
                    "vp",
                    "vice president",
                    "head"
                ]):

                    person_id = person.get("person_id")

                    email = None

                    try:
                        enrich_result = ProspeoService.enrich_person_by_id(
                            person_id
                        )

                        if not enrich_result.get("error"):

                            email = (
                                enrich_result
                                .get("person", {})
                                .get("email", {})
                                .get("email")
                            )

                    except Exception:
                        email = None

                    decision_makers.append({
                        "person_id": person_id,
                        "name": person.get("full_name"),
                        "title": person.get("current_job_title"),
                        "linkedin_url": person.get("linkedin_url"),
                        "email": email
                    })

            results.append({
                "company": {
                    "name": company_data.get("name"),
                    "domain": company_data.get("domain"),
                    "industry": company_data.get("linkedinIndustry"),
                    "employees": company_data.get("employeeCountLinkedin")
                },
                "people": decision_makers
            })

    return render(
        request,
        "home.html",
        {
            "results": results
        }
    )