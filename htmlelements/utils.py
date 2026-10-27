from . import Html
from .element import AnyRenderable as AnyRenderable, SafeStr as SafeStr

DOCTYPE_HTML = SafeStr("<!doctype html>")


def html(*contents: AnyRenderable, **attributes: AnyRenderable) -> str:
    """Renders all passed content inside a Html element.

    Also inserts a doctype tag at the start of the rendered string

    >>> html()
    <!doctype html><html></html>
    """
    return f"{DOCTYPE_HTML}{Html(*contents, **attributes)}"
