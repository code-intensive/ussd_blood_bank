from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from blood_bank.service import UssdService


@csrf_exempt
@require_POST
def ussd(request: HttpRequest) -> HttpResponse:
    return UssdService(request).process_request()
