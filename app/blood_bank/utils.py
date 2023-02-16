from secrets import token_hex

from blood_bank.constants import *
from blood_bank.models import BloodRequest


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
    )
