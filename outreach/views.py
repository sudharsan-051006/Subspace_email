from django.shortcuts import render
from django.http import HttpResponse

from .services.ocean_service import OceanService
from .services.prospeo_service import ProspeoService
from .services.brevo_service import BrevoService
from .services.groq_service import GroqService


def home(request):

    results = []

    if request.method == "POST":

        domain = request.POST.get("domain")
        company_limit = int(
            request.POST.get("company_limit", 5)
        )

        people_limit = int(
            request.POST.get("people_limit", 10)
        )

        ocean_result = (
            OceanService.get_lookalike_companies(
                domain
            )
        )

        companies = ocean_result.get(
            "companies",
            []
        )[:company_limit]

        for company in companies:

            company_data = company.get(
                "company",
                {}
            )

            company_domain = company_data.get(
                "domain"
            )

            if not company_domain:
                continue

            people_result = (
                ProspeoService.search_people(
                    company_domain
                )
            )

            decision_makers = []

            for person_data in people_result.get(
                "results",
                []
            ):

                person = person_data.get(
                    "person",
                    {}
                )

                title = person.get(
                    "current_job_title",
                    ""
                ).lower()

                if any(
                    keyword in title
                    for keyword in [
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
                    ]
                ):

                    email = None

                    try:

                        enrich_result = (
                            ProspeoService
                            .enrich_person_by_id(
                                person.get(
                                    "person_id"
                                )
                            )
                        )

                        if not enrich_result.get(
                            "error"
                        ):

                            email = (
                                enrich_result
                                .get(
                                    "person",
                                    {}
                                )
                                .get(
                                    "email",
                                    {}
                                )
                                .get(
                                    "email"
                                )
                            )

                    except Exception:
                        pass

                    decision_makers.append({
                        "name": person.get(
                            "full_name"
                        ),
                        "title": person.get(
                            "current_job_title"
                        ),
                        "linkedin_url": person.get(
                            "linkedin_url"
                        ),
                        "email": email
                    })

                    if len(
                        decision_makers
                    ) >= people_limit:
                        break

            results.append({
                "company": {
                    "name": company_data.get(
                        "name"
                    ),
                    "domain": company_data.get(
                        "domain"
                    ),
                    "industry": company_data.get(
                        "linkedinIndustry"
                    ),
                    "employees": company_data.get(
                        "employeeCountLinkedin"
                    )
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

def send_selected(request):

    if request.method != "POST":
        return HttpResponse("Invalid Request")

    selected_emails = request.POST.getlist(
        "selected_emails"
    )

    idea = request.POST.get("idea")

    email_data = GroqService.generate_email(
        recipient_name="Decision Maker",
        company_name="Target Company",
        idea=idea
    )

    return render(
        request,
        "bulk_preview.html",
        {
            "emails": selected_emails,
            "subject": email_data["subject"],
            "generated_email": email_data["body"]
        }
    )


def custom_email(request):

    if request.method != "POST":
        return HttpResponse("Invalid Request")

    email = request.POST.get("custom_email")
    name = request.POST.get("custom_name")
    company_name = request.POST.get("company_name")
    idea = request.POST.get("idea")

    email_data = GroqService.generate_email(
        recipient_name=name,
        company_name=company_name,
        idea=idea
    )

    return render(
        request,
        "generated_email.html",
        {
            "email": email,
            "name": name,
            "subject": email_data["subject"],
            "generated_email": email_data["body"]
        }
    )


def send_custom_email(request):

    if request.method != "POST":
        return HttpResponse("Invalid Request")

    email = request.POST.get("email")
    name = request.POST.get("name")

    subject = request.POST.get("subject")

    generated_email = request.POST.get(
        "generated_email"
    )

    result = BrevoService.send_email(
        recipient_email=email,
        recipient_name=name,
        subject=subject,
        html_content=generated_email
    )

    if result.get("success"):
        return HttpResponse(
            "Email Sent Successfully"
        )

    return HttpResponse(
        result.get("error")
    )


def send_generated_email(request):

    if request.method != "POST":
        return HttpResponse("Invalid Request")

    emails = request.POST.getlist("emails")

    subject = request.POST.get("subject")

    generated_email = request.POST.get(
        "generated_email"
    )

    success = 0
    failed = 0

    for email in emails:

        result = BrevoService.send_email(
            recipient_email=email,
            recipient_name=email.split("@")[0],
            subject=subject,
            html_content=generated_email
        )

        if result.get("success"):
            success += 1
        else:
            failed += 1

    return HttpResponse(
        f"""
        Emails Sent: {success}<br>
        Failed: {failed}
        """
    )