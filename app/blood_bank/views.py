from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

CONTENT_TYPE = "text/plain"


@csrf_exempt
@require_POST
def ussd(request: HttpRequest):
    # Read the variables sent via POST from our API
    print(request)
    text = request.POST.get("text", "default")
    session_id = request.session.get("sessionId", None)
    service_code = request.POST.get("serviceCode", None)
    phone_number = request.POST.get("phoneNumber", None)
    name = request.session.get("name", None)
    mobile = request.session.get("mobile", None)
    address = request.session.get("address", None)
    quantity = request.session.get("quantity", None)
    blood_type = request.session.get("blood_type", None)

    response = HttpResponse(content_type=CONTENT_TYPE)

    if request.session.get("requesting", None):
        response.write("CON Select detail to enter")
        if not name:
            response.write("10. Name")
        if not mobile:
            response.write("11. Mobile Number")
        if not address:
            response.write("12. Address")
        if not blood_type:
            response.write("13. Blood type")
        if not quantity:
            response.write("14. Quantity (in pints)")

    if text == "":
        # This is the first request. Note how we start the response with CON
        response.write("CON What would you want to do? \n")
        response.write("1. Request blood \n")
        response.write("2. Donate blood \n")

    elif text == "1":
        request.session["requesting"] = 1
    elif text == "2":
        request.session["donating"] = 1
    elif text in ["1", "1*10"]:
        request.session["name"] = text.strip().lower()
    else:
        response.write("END Invalid choice")

    # Send the response back to the API
    return response 
