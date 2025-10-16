from django.http import HttpRequest
from django.middleware.csrf import get_token

from htmlelements import Input


def csrf_token(request: HttpRequest):
    """Wrapper for django's get_token.

    Returns a callable so that the token can be obtained only when necessary
    """

    def csrf():
        return get_token(request)

    return csrf()


def csrf_input(request: HttpRequest, type="hidden", name="csrfmiddlewaretoken"):
    """A Input[type='hidden'] element with django's csrf_token"""
    return Input(value=csrf_token(request), type=type, name=name)
