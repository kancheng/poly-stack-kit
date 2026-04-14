from rest_framework.response import Response


def ok(data=None, message: str = "OK", status: int = 200) -> Response:
    return Response(
        {"success": True, "message": message, "data": data, "error": None},
        status=status,
    )


def err(message: str, code: int, details=None, status: int | None = None) -> Response:
    http = status or code
    return Response(
        {
            "success": False,
            "message": message,
            "data": None,
            "error": {"code": code, "details": details},
        },
        status=http,
    )
