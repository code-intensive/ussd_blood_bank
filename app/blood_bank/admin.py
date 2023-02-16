from django.contrib import admin

from blood_bank.models import BloodRequest, BankedBlood

admin.site.register((BloodRequest, BankedBlood))
