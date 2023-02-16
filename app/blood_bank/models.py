from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class BloodTypes(models.TextChoices):
    O_POSITIVE = ("o_positive", _("O Positive"))
    O_NEGATIVE = ("o_negative", _("O Negative"))
    A_POSITIVE = ("a_positive", _("A Positive"))
    A_NEGATIVE = ("a_negative", _("A Negative"))
    B_POSITIVE = ("b_positive", _("B Positive"))
    B_NEGATIVE = ("b_negative", _("B Negative"))
    AB_POSITIVE = ("ab_positive", _("AB Positive"))
    AB_NEGATIVE = ("ab_negative", _("AB Negative"))

class BankedBlood(models.Model):
    amount_in_pints = models.PositiveSmallIntegerField(_("amount in pints"))
    blood_type = models.CharField(
        _("blood type"), max_length=50, choices=BloodTypes.choices
    )


class BloodRequest(models.Model):
    address = models.CharField(_("address"), max_length=150)
    full_name = models.CharField(_("full name"), max_length=60)
    mobile = models.CharField(_("mobile number"), max_length=20)
    is_requesting = models.BooleanField(_("is requesting"), default=True)
    amount_in_pints = models.PositiveSmallIntegerField(_("amount in pints"))
    blood_type = models.CharField(
        _("blood type"), max_length=50, choices=BloodTypes.choices
    )
    request_id = models.CharField(_("request id"), max_length=120)
    requesting_number = models.CharField(_("requesting number"), max_length=20)
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.request_id}"
    
