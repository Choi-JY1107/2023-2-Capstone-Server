from django.http import JsonResponse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST


def response(data=None, message=None, status=400):
    status_code = None
    if status == 200:
        status_code = HTTP_200_OK
    if status == 201:
        status_code = HTTP_201_CREATED
    if status == 400:
        status_code = HTTP_400_BAD_REQUEST

    if data is None:
        return JsonResponse(data={"message": message}, status=status_code)
    return JsonResponse(data={"data": data, "message": message}, status=status_code)
