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

    session = request.session
    session.setdefault("name", None)
    session.setdefault("mobile", None)
    session.setdefault("address", None)
    session.setdefault("quantity", None)
    session.setdefault("blood_type", None)

    if not session_id:
        # When session ID is not provided, set it to None to generate a new session key
        session_id = None

    response = HttpResponse(content_type=CONTENT_TYPE)
    if text == "":
        # This is the first request. Note how we start the response with CON
        response.write("CON Welcome to USSD Blood Bank Service")
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
            session["name"] = request_history[LAST_INPUT]
            response.write("Enter your mobile:")
        elif word_count == 3:
            session["mobile"] = request_history[LAST_INPUT]
            response.write("Enter your address:")
        elif word_count == 4:
            session["address"] = request_history[LAST_INPUT]
            session.save()
            response.write(f"END {session['name']}, {session['mobile']}, {session['address']}, {session['blood_type']}")

    elif text == "2":
        session["donating"] = 1
        response.write("CON Enter name")
    else:
        response.write("END Invalid choice")

    session.save()  # Save the session data
    return response

    # Send the response back to the API
