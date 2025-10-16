from . import Html

doctype = "<!doctype html>"


def html(*contents, **atributes):
    """Renders all passed content inside a Html element.

    Also inserts a doctype tag at the start of the rendered string

    >>> html()
    <!doctype html><html></html>
    """
    return doctype + str(Html(*contents, **atributes))
