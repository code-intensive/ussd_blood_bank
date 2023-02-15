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
        response.write("CON What would you want to check \n")
        response.write("1. My Account \n")
        response.write("2. My phone number")

    elif text == "1":
        # Business logic for first level response
        response.write("CON Choose account information you want to view \n")
        response.write("1. Account number")

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
