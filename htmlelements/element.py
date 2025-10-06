from typing import Protocol, Any


def render(value: Any):
    """Returns the value as str.
    If it's a callable, return the result as str

    If it's a boolean, return "true" or "false" (note the lowercase)

    Otherwise, just return the value as str
    """
    if hasattr(value, "__call__"):
        return str(value())
    if value in (True, False):
        return str(value).lower()
    return str(value)


def parse_attribute_tag(attr: str):
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


class Stringfiable(Protocol):
    def __str__(self) -> str: ...


class BaseElement(Stringfiable):
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
        *content: Stringfiable,
        _void=False,
        **attributes,
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

    def __init__(self, *content: Stringfiable, **attributes):
        super().__init__(*content, _void=False, **attributes)


class VoidElement(BaseElement):
    """Element class dedicated to represent void elements

    Similar to Element, but this also ignores anything passed as content
    """

    def __init__(self, *content: Stringfiable, **attributes):
        super().__init__(_void=True, **attributes)
