import unittest
from html import escape

from htmlelements.element import (
    BaseElement,
    Element,
    SafeStr,
    VoidElement,
    parse_attribute_tag,
    render,
)
from htmlelements.utils import html


class DummyForTestRender:
    def __str__(self):
        return "<d>dummy</d>"


class TestRender(unittest.TestCase):
    def test_should_return_SafeStr_unescaped(self):
        s = SafeStr("<d>123</d>")
        self.assertEqual(render(s), s)

    def test_should_escape_regular_str(self):
        s = "<d>123</d>"
        self.assertEqual(render(s), escape(s))

    def test_should_escape_other_types(self):
        d = DummyForTestRender()
        self.assertEqual(render(d), escape(str(d)))

    def test_str_should_not_change(self):
        s = "hello"
        self.assertEqual(s, render(s))

    def test_should_return_callable_result_as_str(self):
        def call_number():
            return 123

        def call_str():
            return "a"

        self.assertEqual(render(call_number), "123")
        self.assertEqual(render(call_str), "a")

    def test_iterables_should_joined_with_spaces(self):
        v = ["class1", "class2"]
        self.assertEqual(render(v), "class1 class2")


class TestParseAttributeTag(unittest.TestCase):

    def test_underscore_to_dash(self):
        self.assertEqual(parse_attribute_tag("some_tag_attr"), "some-tag-attr")

    def test_trailing_dashes_are_removed(self):
        self.assertEqual(parse_attribute_tag("class_"), "class")
        self.assertEqual(parse_attribute_tag("class__"), "class")

    def test_camel_case_to_dash(self):
        self.assertEqual(parse_attribute_tag("MyAttr"), "my-attr")


class TestBaseElement(unittest.TestCase):
    def test_base_element_empty(self):
        el = BaseElement()
        self.assertEqual(str(el), "<base-element></base-element>")

    def test_base_element_with_content(self):
        el = BaseElement("Hello, World!")
        self.assertEqual(str(el), "<base-element>Hello, World!</base-element>")

    def test_base_element_with_attributes(self):
        el = BaseElement(id="myId", class_="myClass", hx_get="endpoint")
        self.assertEqual(
            str(el),
            '<base-element id="myId" class="myClass" hx-get="endpoint"></base-element>',
        )

    def test_base_element_void(self):
        el = BaseElement(_void=True, src="image.png", alt="An image")
        self.assertEqual(str(el), '<base-element src="image.png" alt="An image">')

    def test_base_element_void_with_content(self):
        el = BaseElement("This should be ignored", _void=True)
        self.assertEqual(str(el), "<base-element>")

    def test_attribute_removed_with_value_None(self):
        el = BaseElement(hx_get=None)
        self.assertEqual(str(el), "<base-element></base-element>")

    def test_attribute_removed_with_value_False(self):
        el = BaseElement(hx_get=False)
        self.assertEqual(str(el), "<base-element></base-element>")

    def test_bare_attribute_with_value_True(self):
        el = BaseElement(disabled=True)
        self.assertEqual(str(el), "<base-element disabled></base-element>")

    def test_callable_attribute_returning_True_is_bare(self):
        el = BaseElement(disabled=lambda: True)
        self.assertEqual(str(el), "<base-element disabled></base-element>")

    def test_callable_attribute_returning_False_is_removed(self):
        el = BaseElement(disabled=lambda: False)
        self.assertEqual(str(el), "<base-element></base-element>")

    def test_callable_attribute_returning_None_is_removed(self):
        el = BaseElement(disabled=lambda: None)
        self.assertEqual(str(el), "<base-element></base-element>")

    def test_callable_attribute_is_evaluated_on_each_render(self):
        state = {"disabled": False}
        el = BaseElement(disabled=lambda: state["disabled"])

        self.assertEqual(str(el), "<base-element></base-element>")

        state["disabled"] = True
        self.assertEqual(str(el), "<base-element disabled></base-element>")

    def test_numeric_attributes_are_not_treated_as_booleans(self):
        el = BaseElement(zero=0, one=1)
        self.assertEqual(
            str(el),
            '<base-element zero="0" one="1"></base-element>',
        )

    def test_callable_content(self):
        def call():
            return "hello"

        el = BaseElement(call)
        self.assertEqual(str(el), "<base-element>hello</base-element>")

    def test_callable_attribute_value(self):
        def call():
            return "hello"

        el = BaseElement(data_value=call)
        self.assertEqual(str(el), '<base-element data-value="hello"></base-element>')


class TestElement(unittest.TestCase):
    def test_should_not_be_void(self):
        el = Element()
        self.assertFalse(el._void)


class TestVoidElement(unittest.TestCase):
    def test_should_be_void(self):
        el = VoidElement()
        self.assertTrue(el._void)


class TestUtils(unittest.TestCase):

    def test_html(self):
        el = html(
            "content",
            lang="en",
        )
        expected = '<!doctype html><html lang="en">content</html>'
        self.assertEqual(str(el), expected)


if __name__ == "__main__":
    unittest.main()
