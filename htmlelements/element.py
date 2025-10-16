import html
from typing import Any, Callable, Iterable, Literal


class SafeStr(str):
    """A str that is is not escaped by render.

    All strings as escaped by default. However if you want to pass a string
    that you trust and don't want it to be escaped, wrap it in a SafeStr.
    """

    pass


def render(value: "AnyRenderable") -> str | SafeStr:
    """Returns the value as str.

    If value is a Callable will call render on the result of the call.

    If it's SafeStr it be returned as is

    Booleans are returned as a lowercase str (True => 'true').

    """
    if callable(value):
        return render(value())
    if isinstance(value, SafeStr):
        return value
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, BaseElement):
        return str(value)
    if isinstance(value, str):
        return html.escape(value)
    try:
        iter(value)
        return " ".join(render(v) for v in value)
    except TypeError:
        pass
    # Here value could be anything, call str on it and escape it
    return html.escape(str(value))


TagNames = Literal["classes"] | Literal["label_for"] | str


def parse_attribute_tag(attr: TagNames) -> str:
    """Handles edge cases for element attributes

    Some attributes are keyword in python and will raise errors if attempted to be
    use as named parameters.

    The keywords "class" and "for" are some.

    As such they have been created some special checks to convert:
    classes => class
    label_for => for

    There may be more reserved keywords that have to be handled and
    so this method will be updated to handle them.

    If the attributes are passed from a dictionary expansion, eg **{'class': 'myclass'},
    everything should still work fine

    Additionaly, html element attributes use '-' to represent multi word
    attributes, but you can't have things like 'aria-for' as named parameters.
    Therefore the named parameter should be passed as 'aria_for' and this parser
    will replace '_' with '-'.
    """
    if attr == "classes":
        return "class"
    if attr == "label_for":
        return "for"
    return attr.replace("_", "-")


class BaseElement:
    """Class representing an HTML element.

    Render these objects to html strings by passing to str()

    The attribute 'class' for the html element must be set on the property
    class, since class is a python keyword. Other attributes are set on the
    other_attrs property.

    A Element may be void, in which case it will ommit the closing that
    and any content that it may be holding.
    """

    def __init__(
        self,
        *content: "AnyRenderable",
        _void=False,
        **attributes: "AnyRenderable",
    ):
        self.tag = self.__class__.__name__.lower()
        self._void = _void
        self.content = [] if self._void else content
        self.other_attrs = {parse_attribute_tag(k): v for k, v in attributes.items()}

    def render_attributes(self):
        """Build a string containing all the tag and all of it's attributes.

        Does not include "<" and ">". For instance:
        tag = "a"
        attrs = {"id": "myId"}
        classes = "some-css-class"

        Will produce
        'a id="myId" class="some-css-class"'

        If you call this method directly it's up to you to wrap it in <>
        (maybe with f"<{obj.build_attrs()}>")
        """
        attrs = [self.tag] + [
            f'{key}="{render(value)}"' for key, value in self.other_attrs.items()
        ]
        return " ".join(attrs)

    def __str__(self):
        """Renders the element into a string

        If the element is void, the rendered string will be something like
        <img src="a url"/>

        While a non void element will be
        <button id="myId" class="btn">Click</button>
        """
        attrs = self.render_attributes()
        if self._void:
            return f"<{attrs}>"
        content = "".join(render(c) for c in self.content)
        return f"<{attrs}>{content}</{self.tag}>"


class Element(BaseElement):
    """Element class dedicated to represent non void elements

    It's just a wrapper to remove the _void parameter from __init__
    """

    def __init__(self, *content: "AnyRenderable", **attributes: "AnyRenderable"):
        super().__init__(*content, _void=False, **attributes)


class VoidElement(BaseElement):
    """Element class dedicated to represent void elements

    Similar to Element, but this also ignores anything passed as content
    """

    def __init__(self, *content: "AnyRenderable", **attributes: "AnyRenderable"):
        super().__init__(_void=True, **attributes)


Rendererable = str | SafeStr | bool | BaseElement | Iterable | Any
CallableRenderable = Callable[[], Rendererable]
AnyRenderable = Rendererable | CallableRenderable
