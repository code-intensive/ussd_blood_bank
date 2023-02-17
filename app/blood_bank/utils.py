from datetime import datetime
from secrets import token_hex

from django.db.models.query import QuerySet

from blood_bank.constants import *
from blood_bank.models import BloodRequest, Hospital


def generate_request_id(requesting: bool = True) -> str:
    hex = token_hex(4)
    return f"R_{hex}" if requesting else f"D_{hex}"


def create_request_from_history(
    request_history: list[str], requesting_number: str
) -> BloodRequest:
    is_requesting = request_history[REQUEST_TYPE] == "1"
    name = request_history[NAME_INDEX].strip().title()
    mobile = request_history[MOBILE_INDEX]
    address = request_history[ADDRESS_INDEX].strip().title()
    blood_type_as_int = int(request_history[BLOOD_TYPE_INDEX])
    amount_in_pints = request_history[QUANTITY_INDEX]
    hospital = request_history[HOSPITAL_INDEX]
    blood_type = BLOOD_TYPES_MAP[blood_type_as_int][ACTUAL_BLOOD_TYPE]

    return BloodRequest.objects.create(
        address=address,
        full_name=name,
        mobile=mobile,
        is_requesting=is_requesting,
        request_id=generate_request_id(is_requesting),
        requesting_number=requesting_number,
        blood_type=blood_type,
        amount_in_pints=amount_in_pints,
        hospital=Hospital.objects.get(pk=hospital),
    )


def get_request_history(
    no_of_requests: int = MAX_REQUEST_HISTORY, *, requesting_number: str
) -> QuerySet:
    request_history = BloodRequest.objects.filter(
        requesting_number=requesting_number
    ).values_list("request_id", "date_requested")
    if request_history.count() > no_of_requests:
        return request_history[:no_of_requests]
    return request_history


def format_date_requested(date_requested: datetime) -> str:
    formatted_date = date_requested.strftime(
        "%b %d"
        + "{}, %Y %I:%M%p".format(
            "th"
            if 11 <= date_requested.day <= 13
            else {1: "st", 2: "nd", 3: "rd"}.get(date_requested.day % 10, "th")
        )
    )
    return formatted_date


def build_request_history(request_histories: QuerySet) -> str:
    return "\n".join(
        [
            f"{index}. {request_history[0]} - {format_date_requested(request_history[1])}"
            for index, request_history in enumerate(request_histories, 1)
        ]
    )


def get_available_hospitals() -> str:
    hospitals = Hospital.objects.all()
    return "\n".join([f"{hospital.pk}. {hospital.name}" for hospital in hospitals])


def get_hospital_name_by_id(pk: int) -> str:
    hospital = Hospital.objects.filter(pk=pk).values("name")
    if not hospital:
        return None
    return hospital[0]["name"]
