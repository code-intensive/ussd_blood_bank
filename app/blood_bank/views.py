from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

LAST_INPUT = -1
CONTENT_TYPE = "text/plain"


@csrf_exempt
@require_POST
def ussd(request: HttpRequest) -> HttpResponse:
    text = request.POST.get("text", "default")
    session_id = request.POST.get("sessionId", None)
    service_code = request.POST.get("serviceCode", None)
    phone_number = request.POST.get("phoneNumber", None)

    response = HttpResponse(content_type=CONTENT_TYPE)
    if text == "":
        # This is the first request. Note how we start the response with CON
        response.write("CON Welcome to USSD Blood Bank Service \n")
        response.write("What would you want to do? \n")
        response.write("1. Request blood \n")
        response.write("2. Donate blood \n")

    elif text.startswith("1"):
        request_history = text.split("*")
        word_count = len(request_history)

        if word_count < 4:
            response.write("CON Blood Request: \n")

        if word_count == 1:
            response.write("Enter your name:")
        elif word_count == 2:
            response.write("Enter your mobile:")
        elif word_count == 3:
            response.write("Enter your address:")
        elif word_count == 4:
            response.write(f"END {request_history[1]}, {request_history[2]}, {request_history[3]}, {request_history[4]}")

    elif text == "2":
        response.write("CON Enter name")
    else:
        response.write("END Invalid choice")

    return response

    # Send the response back to the API
