from rest_framework.views import exception_handler
from rest_framework.response import Response

from common.errors.exceptions import BusinessException
from common.errors.error_map import ERROR_MAP
from common.errors.error_codes import ErrorCode


def global_exception_handler(exc, context):
    if isinstance(exc, BusinessException):
        spec = ERROR_MAP[exc.error_code.value]
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
        return Response(
            {
                "status": response.status_code,
                "code": "FrameworkError",
                "message": response.data,
            },
            status=response.status_code,
        )

    spec = ERROR_MAP[ErrorCode.INTERNAL_ERROR.value]
    return Response(
        {
            "status": spec["status"],
            "code": spec["code"],
            "message": spec["message"],
        },
        status=spec["status"],
    )