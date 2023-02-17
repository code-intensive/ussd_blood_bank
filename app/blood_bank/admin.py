from django.contrib import admin

from blood_bank.models import BankedBlood, BloodRequest, Hospital

admin.site.register((BloodRequest, BankedBlood, Hospital))
