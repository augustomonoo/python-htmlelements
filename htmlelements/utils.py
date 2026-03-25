from typing import Any

from . import Html
from .element import AnyRenderable

doctype = "<!doctype html>"


def html(*contents: AnyRenderable, **attributes: AnyRenderable) -> str:
    """Renders all passed content inside a Html element.

    Also inserts a doctype tag at the start of the rendered string

    >>> html()
    <!doctype html><html></html>
    """
    return doctype + str(Html(*contents, **attributes))
