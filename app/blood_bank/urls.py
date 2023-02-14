from blood_bank.views import ussd
from django.urls import path

urlpatterns = [path("ussd/", ussd, name="ussd")]
