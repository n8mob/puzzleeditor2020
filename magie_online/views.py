import uuid

from django.http import HttpResponse


def index(request):
    serial_number = uuid.uuid5(uuid.NAMESPACE_DNS, request.get_host())
    return HttpResponse(serial_number)
