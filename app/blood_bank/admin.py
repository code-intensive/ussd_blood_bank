from blood_bank.models import (
    BankedBlood,
    BloodRequest,
    Hospital,
    Donor,
    Recipient,
    Appointment,
)
from django.contrib import admin

admin.site.register((BloodRequest, BankedBlood, Hospital))
