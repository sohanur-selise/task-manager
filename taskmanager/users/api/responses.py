from django.http import JsonResponse


def base_object(success=True, data=[], errors=[], message=""):
    return {
        "success": success,
        "data": data,
        "errors": errors,
        "message": message,
    }


def error(errors={}, status_code=400, message=""):
    return JsonResponse(
        base_object(success=False, errors=errors, message=message),
        status=status_code,
        safe=False,
    )


def success(data=[], status_code=200, message=""):
    return JsonResponse(
        base_object(success=True, data=data, message=message),
        status=status_code,
        safe=False,
    )
