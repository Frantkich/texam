from flask import Response
from flask_login import current_user
import json


def return_data(data: dict) -> Response:
    """
    Returns a Flask Response object with the data.

    Args:
        data (dict): The data to return.

    Returns:
        Response: Flask Response object with the data.
    """
    return Response(json.dumps(data), 200, content_type="application/json")


def return_error(error_code: int, msg: str = "") -> Response:
    """
    Returns a Flask Response object with an error message.

    Args:
        error_code (int): The HTTP status code for the error.
        msg (str, optional): The error message. Defaults to "".

    Returns:
        Response: Flask Response object with an error message.
    """
    return Response(json.dumps({"status": "error", "message": msg}), error_code, content_type="application/json")

def return_success(msg: str = "") -> Response:
    """
    Returns a Flask Response object with an success message.

    Args:
        msg (str, optional): The success message. Defaults to "".

    Returns:
        Response: Flask Response object with an success message.
    """
    return Response(json.dumps({"status": "success", "message": msg}), 200, content_type="application/json")


def user_is_admin() -> bool:
    """
    Checks if the current user is an admin.

    Returns:
        bool: True if the current user is an admin, False otherwise.
    """
    return current_user.role == 1 
