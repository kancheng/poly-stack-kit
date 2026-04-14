from rest_framework.views import exception_handler


def polystack_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        status = response.status_code
        detail = response.data
        msg = "Error"
        if isinstance(detail, dict) and "detail" in detail:
            msg = str(detail["detail"])
        elif isinstance(detail, list):
            msg = "; ".join(str(x) for x in detail)
        elif isinstance(detail, dict):
            msg = next(iter(detail.keys()), "Validation error")
        response.data = {
            "success": False,
            "message": msg,
            "data": None,
            "error": {"code": status, "details": detail},
        }
    return response
