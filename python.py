from outreach.services.brevo_service import BrevoService

result = BrevoService.send_email(
    recipient_email="sudharsanreddy.saragada@gmail.com",
    recipient_name="Sudharsan"
)

print(result)