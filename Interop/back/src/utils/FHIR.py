import os

from fhirclient import client

settings = {
    'app_id': os.environ.get("APP_ID"),
    'api_base': os.environ.get("API_BASE_URL"),
}


def smart_request():
    return client.FHIRClient(settings=settings)
