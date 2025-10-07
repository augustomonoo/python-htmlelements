import unittest
from html import escape

from htmlelements.dynamic import VOID_ELEMENTS, get_element, make_element
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

    def test_should_return_bools_as_lowercase_str(self):
        self.assertEqual(render(True), "true")
        self.assertEqual(render(False), "false")


class TestParseAttributeTag(unittest.TestCase):
    def test_classes_to_class(self):
        self.assertEqual(parse_attribute_tag("classes"), "class")

    def test_label_for_to_label(self):
        self.assertEqual(parse_attribute_tag("label_for"), "for")

    def test_underscore_to_dash(self):
        self.assertEqual(parse_attribute_tag("some_tag_attr"), "some-tag-attr")


class TestBaseElement(unittest.TestCase):
    def test_base_element_empty(self):
        el = BaseElement()
        self.assertEqual(str(el), "<baseelement></baseelement>")

    def test_base_element_with_content(self):
        el = BaseElement("Hello, World!")
        self.assertEqual(str(el), "<baseelement>Hello, World!</baseelement>")

    def test_base_element_with_attributes(self):
        el = BaseElement(id="myId", classes="myClass", hx_get="endpoint")
        self.assertEqual(
            str(el),
            '<baseelement id="myId" class="myClass" hx-get="endpoint"></baseelement>',
        )

    def test_base_element_void(self):
        el = BaseElement(_void=True, src="image.png", alt="An image")
        self.assertEqual(str(el), '<baseelement src="image.png" alt="An image">')

    def test_base_element_void_with_content(self):
        el = BaseElement("This should be ignored", _void=True)
        self.assertEqual(str(el), "<baseelement>")

    def test_base_element_void_with_attributes(self):
        el = BaseElement(_void=True, id="voidId", classes="voidClass")
        self.assertEqual(str(el), '<baseelement id="voidId" class="voidClass">')

    def test_attribute_classes(self):
        el = BaseElement(classes="class1 class2")
        self.assertIn('class="class1 class2"', str(el))

    def test_attribute_label_for(self):
        el = BaseElement(label_for="inputId")
        self.assertIn('for="inputId"', str(el))

    def test_attribute_replace_underscores(self):
        el = BaseElement(hx_get="url")
        self.assertIn('hx-get="url"', str(el))

    def test_callable_content(self):
        def call():
            return "hello"

        el = BaseElement(call)
        self.assertEqual(str(el), "<baseelement>hello</baseelement>")

    def test_callalbe_attribute_value(self):
        def call():
            return "hello"

        el = BaseElement(data_value=call)
        self.assertEqual(str(el), '<baseelement data-value="hello"></baseelement>')


class TestElement(unittest.TestCase):
    def test_should_be_void(self):
        el = Element()
        self.assertFalse(el._void)


class TestVoidElement(unittest.TestCase):
    def test_should_be_void(self):
        el = VoidElement()
        self.assertTrue(el._void)


class TestMakeELement(unittest.TestCase):
    def test_make_element(self):
        Div = make_element("Div", Element)
        self.assertTrue(issubclass(Div, Element))

    def test_make_void_element(self):
        Img = make_element("Img", VoidElement)
        self.assertTrue(issubclass(Img, VoidElement))

    def test_should_cache_created_classes(self):
        Div1 = make_element("Div", Element)
        Div2 = make_element("Div", Element)
        self.assertIs(Div1, Div2)

    def test_created_element_should_be_named(self):
        name = "div"
        Div = make_element(name, Element)
        self.assertEqual(Div.__name__, name.capitalize())


class TestGetElement(unittest.TestCase):
    def test_should_return_void_element(self):
        for element in VOID_ELEMENTS:
            el = get_element(element)
            self.assertTrue(issubclass(el, VoidElement))

    def test_should_return_element(self):
        Div = get_element("div")
        self.assertTrue(issubclass(Div, Element))


class TestDynamicImport(unittest.TestCase):

    def test_element(self):
        from htmlelements.dynamic import Div

        self.assertTrue(issubclass(Div, Element))

    def test_void_element(self):
        from htmlelements.dynamic import Img

        self.assertTrue(issubclass(Img, VoidElement))


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
