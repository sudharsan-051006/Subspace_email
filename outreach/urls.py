from django.urls import path
from .views import (
    home,
    send_custom_email,
    send_generated_email,
    send_selected,
    custom_email
)

urlpatterns = [
    path("", home),
        path(
        "send-selected/",
        send_selected,
        name="send_selected"
    ),
    path(
        "custom-email/",
        custom_email,
        name="custom_email"
    ),

    path(
    "send-generated-email/",
    send_generated_email,
    name="send_generated_email"
    ),

    path(
    "send-custom-email/",
    send_custom_email,
    name="send_custom_email"
    ),
]