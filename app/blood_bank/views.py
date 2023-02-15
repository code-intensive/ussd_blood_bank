from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

CONTENT_TYPE = "text/plain"


@csrf_exempt
@require_POST
def ussd(request):
    # Read the variables sent via POST from our API
    text = request.POST.get("text", "default")
    session_id = request.session.get("sessionId", None)
    service_code = request.POST.get("serviceCode", None)
    phone_number = request.POST.get("phoneNumber", None)

    response = HttpResponse(content_type=CONTENT_TYPE)

    if text == "":
        # This is the first request. Note how we start the response with CON
        response.write("CON What would you want to do? \n")
        response.write("1. Request blood \n")
        response.write("2. Donate blood \n")

    elif text == "1":
        # Business logic for first level response
        name = request.session.get("name", None)
        mobile = request.session.get("mobile", None)
        address = request.session.get("address", None)
        if not name:
            if text != "1":
                request.session["name"] = text.strip().title()
                response.write("CON Enter your mobile \n")
            else:
                response.write("CON Enter your name \n")
        elif not mobile:
            if text != "1":
                request.session["mobile"] = text.strip()
                response.write("CON Enter your address \n")
            else:
                response.write("CON Enter your mobile \n")
        else:
            response.write(f"END Your name is { name } and your mobile is { mobile }")
        # elif not address:
        #     if text != "1":
        #         request.session["address"] = text.strip().capitalize()
        #         response.write("CON Enter your mobile \n")
        #     else:
        #         response.write("CON Select blood type")
        #         response.write("1) O Positive")
        #         response.write("2) O Negative")
        #         response.write("3) A Positive")
        #         response.write("4) A Negative")
        #         response.write("5) B Positive")
        #         response.write("6) B Negative")
        #         response.write("7) AB Positive")
        #         response.write("8) AB Negative")
        # else:

    elif text == "2":
        # This is a terminal request. Note how we start the response with END
        response.write(f"END Your phone number is { phone_number }")

    elif text == "1*1":
        # This is a second level response where the user selected 1 in the first instance
        account_number = "ACC1001"
        # This is a terminal request. Note how we start the response with END
        response.write(f"END Your account number is { account_number }")

    else:
        response.write("END Invalid choice")

    # Send the response back to the API
    return response
