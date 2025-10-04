"""Dynamically generate tags by hooking the module's __getattr__
Idea taken from FastHTML

Documentation on module __getattr__ is available here
https://docs.python.org/3/reference/datamodel.html#module.__getattr__
"""

from typing import TypeVar

from .element import Element, VoidElement

# https://developer.mozilla.org/en-US/docs/Glossary/Void_element
VOID_ELEMENTS = (
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
)


# @cache was breaking type hints :(
__element_cache: dict[tuple[str, type], type] = {}

T = TypeVar("T", bound=Element | VoidElement)


def make_element(tag: str, parent_class: type[T], use_cache=True) -> type[T]:
    """Creates a HTML Element class with the given tag name and parent class.

    Will cache the created class based on tag and parent_class.
    Note: this function uses a rather simple cache instead of itertools.cache
    since the that was breaking type hints.
    """
    key = (tag, parent_class)
    if use_cache and key not in __element_cache:
        capitalized = tag.capitalize()
        DynamicElement = type(capitalized, (parent_class,), {})
        DynamicElement.__name__ = capitalized
        __element_cache[key] = DynamicElement
    return __element_cache[key]


def get_element(tag: str):
    """Get an HTML element class by its tag name.

    If the required element is a void element (ie. has no content), the returned
    class will be a subclass of VoidElement. Otherwise, it will be a subclass
    of Element.
    More information on Void Elements:
    https://developer.mozilla.org/en-US/docs/Glossary/Void_element
    """
    parent_class = VoidElement if tag.lower() in VOID_ELEMENTS else Element
    return make_element(tag, parent_class)


def __getattr__(tag: str):
    return get_element(tag)
