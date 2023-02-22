from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class BloodType(models.TextChoices):
    O_POSITIVE = ("o_positive", _("O Positive"))
    O_NEGATIVE = ("o_negative", _("O Negative"))
    A_POSITIVE = ("a_positive", _("A Positive"))
    A_NEGATIVE = ("a_negative", _("A Negative"))
    B_POSITIVE = ("b_positive", _("B Positive"))
    B_NEGATIVE = ("b_negative", _("B Negative"))
    AB_POSITIVE = ("ab_positive", _("AB Positive"))
    AB_NEGATIVE = ("ab_negative", _("AB Negative"))


class Hospital(models.Model):
    name = models.CharField(_("name"), max_length=60)
    address = models.CharField(_("address"), max_length=150)
    help_line = models.CharField(_("help line"), max_length=20)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class BankedBlood(models.Model):
    amount_in_pints = models.PositiveSmallIntegerField(_("amount in pints"))
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="banked_blood"
    )
    blood_type = models.CharField(
        _("blood type"), max_length=50, choices=BloodType.choices
    )

    class Meta:
        unique_together = ["hospital", "blood_type"]

    def __str__(self):
        return self.blood_type


class BloodRequest(models.Model):
    class Meta:
        ordering = ["-date_requested"]
        indexes = [
            models.Index(
                fields=[
                    "full_name",
                    "mobile",
                    "is_requesting",
                    "blood_type",
                    "request_id",
                    "date_requested",
                    "requesting_number",
                ]
            )
        ]

    full_name = models.CharField(_("full name"), max_length=60)
    address = models.CharField(_("address"), max_length=150)
    mobile = models.CharField(_("mobile number"), max_length=20)
    amount_in_pints = models.PositiveSmallIntegerField(_("amount in pints"))
    blood_type = models.CharField(
        _("blood type"), max_length=50, choices=BloodType.choices
    )
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="blood_requests"
    )
    is_requesting = models.BooleanField(_("is requesting"), default=True)
    request_id = models.CharField(_("request id"), max_length=120)
    requesting_number = models.CharField(_("requesting number"), max_length=20)
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.request_id}"


class Person(models.Model):
    class Meta:
        abstract = True

    full_name = models.CharField(_("full name"), max_length=60)
    amount_in_pints = models.PositiveSmallIntegerField(_("amount in pints"))
    blood_type = models.CharField(
        _("blood type"), max_length=50, choices=BloodType.choices
    )


class Donor(Person):
    date_donated = models.DateTimeField(auto_now_add=True)


class Recipient(Person):
    date_received = models.DateTimeField(auto_now_add=True)


class Appointment(models.Model):
    scheduled_for = models.DateTimeField()
