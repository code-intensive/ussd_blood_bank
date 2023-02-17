from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from blood_bank.constants import *
from blood_bank.utils import (
    build_request_history,
    create_request_from_history,
    get_request_history,
    get_available_hospitals,
    get_hospital_name_by_id,
)


@csrf_exempt
@require_POST
def ussd(request: HttpRequest) -> HttpResponse:
    text = request.POST.get("text", "default")
    session_id = request.POST.get("sessionId", None)
    service_code = request.POST.get("serviceCode", None)
    requesting_number = request.POST.get("phoneNumber", None)

    response = HttpResponse(content_type=CONTENT_TYPE)

    if text == "":
        # This is the first request. Note how we start the response with CON
        response.write(
            "CON Welcome to USSD Blood Bank Service \n"
            "1. Request blood \n"
            "2. Donate blood \n"
            "3. Request management"
        )

    elif text[0] in ["1", "2"]:
        request_histories = [
            request_input for request_input in text.split("*") if request_input
        ]
        word_count = len(request_histories)

        if word_count == NAME_INDEX:
            response.write("CON Enter name: \n")
        elif word_count == MOBILE_INDEX:
            response.write("CON Enter mobile: \n")
        elif word_count == ADDRESS_INDEX:
            response.write("CON Enter address: \n")
        elif word_count == BLOOD_TYPE_INDEX:
            response.write("CON Select blood type: \n")
            for blood_type_index, blood_type in BLOOD_TYPES_MAP.items():
                response.write(
                    f"{blood_type_index}. {blood_type[HUMAN_READABLE_BLOOD_TYPE]} \n"
                )
        elif word_count == QUANTITY_INDEX:
            response.write("CON Enter quantity (in pints): \n")
        elif word_count == HOSPITAL_INDEX:
            response.write("CON Select hospital: \n")
            response.write(get_available_hospitals())
        elif word_count == DATA_INTEGRITY:
            request_type = (
                "request" if request_histories[REQUEST_TYPE] == "1" else "donation"
            )
            name = request_histories[NAME_INDEX].strip().title()
            mobile = request_histories[MOBILE_INDEX]
            address = request_histories[ADDRESS_INDEX].strip().capitalize()
            blood_type_as_int = int(request_histories[BLOOD_TYPE_INDEX])
            hospital = request_histories[HOSPITAL_INDEX]
            amount_in_pints = request_histories[QUANTITY_INDEX]
            blood_type = BLOOD_TYPES_MAP[blood_type_as_int][HUMAN_READABLE_BLOOD_TYPE]
            response.write(
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
        elif word_count == END_OF_REQUEST_INDEX:
            proceed = request_histories[CONFIRMED_INTEGRITY] == "1"
            if proceed:
                blood_request = create_request_from_history(
                    request_histories, requesting_number
                )
                response.write("END Request created successfully \n")
                response.write(blood_request.request_id)
            else:
                response.write("END Requested terminated.")
        else:
            response.write("Invalid requests")
    elif text.startswith("3"):
        request_histories = [
            request_input for request_input in text.split("*") if request_input
        ]
        word_count = len(request_histories)
        if word_count == 1:
            response.write(
                "CON Request History \n\n"
                "1. View requests \n"
                "2. Find request or appointment"
                "3. View appointments \n"
                "4. Cancel request \n"
                "5. Cancel appointment"
            )
        elif text == "3*1":
            request_history = get_request_history(requesting_number=requesting_number)
            if not request_history:
                response.write("END You have not made any requests.")
            else:
                request_count = request_history.count()
                no_of_requests = (
                    MAX_REQUEST_HISTORY
                    if request_count > MAX_REQUEST_HISTORY
                    else request_count
                )
                response.write(f"END Showing last {no_of_requests} requests \n\n")
                response.write(build_request_history(request_histories))
    else:
        response.write("END Invalid choice")

    return response

    # Send the response back to the API


0
