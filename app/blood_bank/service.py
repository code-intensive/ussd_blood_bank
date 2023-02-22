from django.http import HttpRequest, HttpResponse

from blood_bank.constants import *
from blood_bank.utils import (
    build_history,
    create_request_from_history,
    display_details_from_iterable,
    display_details_from_model,
    find_blood_request_by_id,
    find_donation_request_by_id,
    delete_donation_request_by_id,
    get_available_hospitals,
    get_donation_history,
    get_hospital_name_by_id,
    get_request_history,
)


class UssdService:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request

    def process_request(self) -> HttpResponse:
        text = self.request.POST.get("text", "default")
        session_id = self.request.POST.get("sessionId", None)
        service_code = self.request.POST.get("serviceCode", None)
        requesting_number = self.request.POST.get("phoneNumber", None)

        response = HttpResponse(content_type=CONTENT_TYPE)

        if text == "":
            # This is the first request. Note how we start the response with CON
            response.write(
                "CON Welcome to USSD Blood Bank Service \n\n"
                "1. Request blood \n"
                "2. Donate blood \n"
                "3. Manage my activities"
            )
        elif text[0] in ["1", "2"]:
            request_histories = [
                request_input for request_input in text.split("*") if request_input
            ]
            hop_count = len(request_histories)

            if hop_count == NAME_INDEX:
                response.write("CON Enter name: \n")
            elif hop_count == MOBILE_INDEX:
                response.write("CON Enter mobile: \n")
            elif hop_count == ADDRESS_INDEX:
                response.write("CON Enter address: \n")
            elif hop_count == BLOOD_TYPE_INDEX:
                response.write("CON Select blood type: \n")
                for blood_type_index, blood_type in INT_BLOOD_TYPES_MAP.items():
                    response.write(
                        f"{blood_type_index}. {blood_type[HUMAN_READABLE_BLOOD_TYPE]} \n"
                    )
            elif hop_count == QUANTITY_INDEX:
                response.write("CON Enter quantity (in pints): \n")
            elif hop_count == HOSPITAL_INDEX:
                response.write("CON Select hospital: \n")
                response.write(get_available_hospitals())
            elif hop_count == DATA_INTEGRITY:
                response.write(display_details_from_iterable(request_histories))
            elif hop_count == END_OF_REQUEST_INDEX:
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
                response.write("Invalid request")
        elif text.startswith("3"):
            request_histories = [
                request_input for request_input in text.split("*") if request_input
            ]
            hop_count = len(request_histories)
            if text == "3":
                response.write(
                    "CON What do you want to manage? \n\n"
                    "1. Requests \n"
                    "2. Donations \n"
                    "3. Appointments \n"
                )
            elif text.startswith("3*1"):
                if text == "3*1":
                    response.write(
                        "CON Requests \n\n"
                        "1. View most recent requests \n"
                        "2. Search request by ID \n"
                        "3. Cancel a request \n"
                    )
                elif text == "3*1*1":
                    request_history = get_request_history(
                        requesting_number=requesting_number
                    )
                    if not request_history:
                        response.write("END You currently have no active requests.")
                    else:
                        response.write(
                            f"END Showing last {request_history.count()} request(s) made \n\n"
                        )
                        response.write(build_history(request_history))
                elif text.startswith("3*1*2"):
                    if text == "3*1*2":
                        response.write("CON Enter request ID")
                    else:
                        request_id = request_histories[LAST_INPUT_INDEX]
                        blood_request = find_blood_request_by_id(
                            request_id,
                            requesting_number=requesting_number,
                        )
                        if not blood_request:
                            response.write("END Blood request not found")
                        else:
                            response.write("END Blood Request Details \n\n")
                            response.write(display_details_from_model(blood_request))
                elif text.startswith("3*1*3"):
                    if text == "3*1*3":
                        response.write("CON Enter request ID")
                    elif hop_count == 4:
                        request_id = request_histories[LAST_INPUT_INDEX]
                        blood_request = find_blood_request_by_id(
                            request_id, requesting_number=requesting_number
                        )
                        if not blood_request:
                            response.write("END Blood request not found")
                        else:
                            response.write("CON Proceed with deletion? \n\n")
                            response.write(display_details_from_model(blood_request))
                            response.write("1. Yes \n" "2. No \n")
                    elif hop_count == 5:
                        should_not_delete = request_histories[LAST_INPUT_INDEX] == "2"
                        if should_not_delete:
                            response.write("END Request deletion aborted")
                        else:
                            request_id = request_histories[-2]
                            blood_request = delete_blood_request_by_id(
                                request_id, requesting_number=requesting_number
                            )
                            response.write(f"END Successfully deleted {request_id}")

                    else:
                        response.write("END Invalid request")
                else:
                    response.write("END Invalid request")
            elif text.startswith("3*2"):
                donation_histories = [
                    request_input for request_input in text.split("*") if request_input
                ]
                hop_count = len(donation_histories)
                if text == "3*2":
                    response.write(
                        "CON Donations \n\n"
                        "1. View most recent donations \n"
                        "2. Search donation by ID \n"
                        "3. Cancel a donation \n"
                    )
                elif text == "3*2*1":
                    donation_history = get_donation_history(
                        requesting_number=requesting_number
                    )
                    if not donation_history:
                        response.write(
                            "END You have not requested to make donation(s)."
                        )
                    else:
                        response.write(
                            f"END Showing last {donation_history.count()} donation(s) made \n\n"
                        )
                        response.write(build_history(donation_history))
                elif text.startswith("3*2*2"):
                    if text == "3*2*2":
                        response.write("CON Enter donation ID")
                    else:
                        donation_id = donation_histories[LAST_INPUT_INDEX]
                        blood_donation = find_donation_request_by_id(
                            donation_id,
                            requesting_number=requesting_number,
                        )
                        if not blood_donation:
                            response.write("END Blood donation not found")
                        else:
                            response.write("END Blood Donation Details \n\n")
                            response.write(display_details_from_model(blood_donation))
                elif text.startswith("3*2*3"):
                    if text == "3*2*3":
                        response.write("CON Enter donation ID")
                    elif hop_count == 4:
                        donation_id = donation_histories[LAST_INPUT_INDEX]
                        blood_donation = find_donation_request_by_id(
                            donation_id, requesting_number=requesting_number
                        )
                        if not blood_donation:
                            response.write("END Blood donation not found")
                        else:
                            response.write("CON Proceed with deletion? \n\n")
                            response.write(display_details_from_model(blood_donation))
                            response.write("1. Yes \n" "2. No \n")
                    elif hop_count == 5:
                        should_not_delete = donation_histories[LAST_INPUT_INDEX] == "2"
                        if should_not_delete:
                            response.write("END Request deletion aborted")
                        else:
                            donation_id = donation_histories[-2]
                            blood_donation = delete_donation_request_by_id(
                                donation_id, requesting_number=requesting_number
                            )
                            response.write(f"END Successfully deleted {donation_id}")
                else:
                    response.write("END Invalid donation")
        else:
            response.write("END Invalid choice")

        return response
