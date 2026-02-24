from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import exception_handler

from common.errors.error_codes import ErrorCode
from common.errors.error_map import ERROR_MAP
from common.errors.exceptions import BusinessException


def global_exception_handler(exc, context):

    if isinstance(exc, BusinessException):
        spec = ERROR_MAP.get(
            exc.error_code.value,
            ERROR_MAP[ErrorCode.INTERNAL_ERROR.value],
        )
        return Response(
            {
                "status": spec["status"],
                "code": spec["code"],
                "message": spec["message"],
            },
            status=spec["status"],
        )

    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            "status": response.status_code,
            "code": "FrameworkError",
            "message": str(response.data),
        }
        return response

    spec = ERROR_MAP[ErrorCode.INTERNAL_ERROR.value]
    return Response(
        {
            "status": spec["status"],
        "code": spec["code"],
            "message": spec["message"],
        },
        status=spec["status"],
    )