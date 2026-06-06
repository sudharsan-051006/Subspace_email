from django.urls import path
from .views import home

urlpatterns = [
    path("", home),
    # path("company/", company_details, name="company_details"),
]