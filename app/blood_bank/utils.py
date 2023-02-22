from datetime import datetime
from secrets import token_hex
from typing import Iterable

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
    blood_type = INT_BLOOD_TYPES_MAP[blood_type_as_int][ACTUAL_BLOOD_TYPE]

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


def _get_history(
    no_of_requests: int = MAX_REQUEST_HISTORY,
    *,
    requesting_number: str,
    is_requesting: bool,
) -> QuerySet:
    request_history = BloodRequest.objects.filter(
        requesting_number=requesting_number, is_requesting=is_requesting
    ).values_list("request_id", "date_requested")
    if request_history.count() > no_of_requests:
        return request_history[:no_of_requests]
    return request_history


def get_request_history(
    no_of_requests: int = MAX_REQUEST_HISTORY, *, requesting_number: str
) -> QuerySet:
    return _get_history(requesting_number=requesting_number, is_requesting=True)


def get_donation_history(
    no_of_requests: int = MAX_REQUEST_HISTORY, *, requesting_number: str
) -> QuerySet:
    return _get_history(requesting_number=requesting_number, is_requesting=False)


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


def build_history(histories: QuerySet) -> str:
    return "\n".join(
        [
            f"{index}. {history[0]} - {format_date_requested(history[1])}"
            for index, history in enumerate(histories, 1)
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


def display_details_from_iterable(request_histories: Iterable) -> str:
    request_type = "request" if request_histories[REQUEST_TYPE] == "1" else "donation"
    name = request_histories[NAME_INDEX].strip().title()
    mobile = request_histories[MOBILE_INDEX]
    address = request_histories[ADDRESS_INDEX].strip().capitalize()
    blood_type_as_int = int(request_histories[BLOOD_TYPE_INDEX])
    hospital = request_histories[HOSPITAL_INDEX]
    amount_in_pints = request_histories[QUANTITY_INDEX]
    blood_type = INT_BLOOD_TYPES_MAP[blood_type_as_int][HUMAN_READABLE_BLOOD_TYPE]
    return (
        f"CON BLOOD { request_type.upper() } \n\n"
        f"Name: {name} \n"
        f"Mobile: {mobile} \n"
        f"Address: {address} \n"
        f"Blood type: {blood_type} \n"
        f"Quantity (in pints): {amount_in_pints} \n"
        f"Hospital: {get_hospital_name_by_id(hospital)} \n\n"
        "Is the above data correct?\n\n"
        "1. Yes \n"
        "2. No"
    )


def display_details_from_model(blood_request: BloodRequest) -> str:
    return (
        f"Name: {blood_request.full_name} \n"
        f"Mobile: {blood_request.mobile} \n"
        f"Address: {blood_request.address} \n"
        f"Blood type: {BLOOD_TYPES_MAP[blood_request.blood_type]} \n"
        f"Quantity (in pints): {blood_request.amount_in_pints} \n"
        f"Hospital: {blood_request.hospital.name} \n"
        f"Date Requested: {format_date_requested(blood_request.date_requested)} \n\n"
    )


def find_request_by_id(
    request_id: str, *, requesting_number: str, is_requesting: bool
) -> BloodRequest | None:
    return BloodRequest.objects.filter(
        request_id=request_id,
        requesting_number=requesting_number,
        is_requesting=is_requesting,
    ).first()


def find_blood_request_by_id(request_id: str, requesting_number) -> str:
    return find_request_by_id(
        request_id, requesting_number=requesting_number, is_requesting=True
    )


def find_donation_request_by_id(request_id: str, requesting_number) -> str:
    return find_request_by_id(
        request_id, requesting_number=requesting_number, is_requesting=False
    )


def delete_request_by_id(
    request_id: str, *, requesting_number: str, is_requesting: bool
) -> BloodRequest | None:
    return (
        BloodRequest.objects.filter(
            request_id=request_id,
            requesting_number=requesting_number,
            is_requesting=is_requesting,
        )
        .first()
        .delete()
    )


def delete_blood_request_by_id(request_id: str, requesting_number) -> str:
    return delete_request_by_id(
        request_id, requesting_number=requesting_number, is_requesting=True
    )


def delete_donation_request_by_id(request_id: str, requesting_number) -> str:
    return delete_request_by_id(
        request_id, requesting_number=requesting_number, is_requesting=False
    )
