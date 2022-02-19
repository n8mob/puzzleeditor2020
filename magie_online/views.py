import json
import uuid
from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse


def index(request):
    host = request.get_host()
    uuid_for_host = str(uuid.uuid5(uuid.NAMESPACE_DNS, host))
    timestamp = datetime.now()

    response = {
        'my_uuid': uuid_for_host,
        'timestamp': timestamp,
    }

    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))
