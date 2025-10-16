# HTML Elements

Create HTML using python code. Inspired by [FastHTML](https://fastht.ml/).

I really enjoy working with [Django](https://djangoproject.com), but really
dislike the templating.

I've used some JSX, and really liked it, but that meant going JS/TS.

Then I saw FastHTML. Specifically, it's [ft components](https://fastht.ml/docs/explains/explaining_xt_components.html). And loved it.

And tried using it within Django, and it worked fine! The only issue is
pulling the entire FastHTML as a dependency, which is not very nice.

So I decided to write something very similar, just focused on generating
HTML.

And here it is:

```python
>>> from htmlelements import Head, Title, Body, H1
>>> from htmlelements.utils import html

>>> html(
  Head(Title("My Title")),
  Body(H1("My Heading", classes="h1")),
  )
'<!doctype html><html><head><title>My Title</title></head><body><h1 class="h1">My Heading</h1></body></html>'

```

Very simple (most of the lines in the python module are comments). Should
also be very easy to modify if any specific functionality is needed.

## Quick start

Import the element you want from `htmlelements`.

Instantiate the element. Any keyword argument passed will be added to the
element attributes. Other arguments are passed as children for the element. If
the element imported is a void element, such as img, then anything passed as
child will be ignored.

Render the element with `str`. Or just print it to the terminal.

```python

>>> from htmlelements import Div, P

>>> str(Div(
  P(
    "Hello World",
    classes="p-classes",
    ),
  classes="div-class",
))
'<div class="div-class"><p class="p-class">Hello World</p></div>'
```

Some elements are considered [Void Element](https://developer.mozilla.org/en-US/docs/Glossary/Void_element),
as in: they do not have any child node.

These void elements are subclasses of `VoidElement`. Any
non-keyword parameter will be ignored when instantiating them

```python
>>> from htmlelements import Img, P
>>> str(Img(P("This will be ignored")))
'<img>'
```

Note that void elements are not self closing since [self closing tags do not
exists in HTML](https://developer.mozilla.org/en-US/docs/Glossary/Void_element#self-closing_tags)

## HTML Escaping

Any value passed as attribute or child is escaped using Python's built-in
[`html.escape`](https://docs.python.org/3/library/html.html#html.escape)

Callables will have they return value passed back to the rendering function.

If you want have a value not be escaped use `htmlelements.element.SafeStr`.
It's just a wrapper for regular strings, but this is returned as is by
the render function.

```python
>>> from htmlelements.element import SafeStr, render
>>> escaped = "<p>sample</p>"
>>> render(escaped)
'&lt;p&gt;sample&lt;/p&gt;'
>>> not_escaped = SafeStr(escaped)
>>> render(not_escaped)
'<p>sample</p>'
```

## The utils module

The utils module has just two things for now: `doctype` and a function `html`

The `doctype` is just the string `'<!doctype html>'`.

The `html` function wraps a `Html` element class and returns it rendered as a
string with the doctype prepended

```python
>>> from htmlelements.utils import html
>>> str(html("Other HTML elements go here"))
'<!doctype html><html>Other HTML elements go here</html>'
```

## The classes: BaseElement, Element and VoidElement

Do not use these classes directly. Use them to create new classes!

If you do instantiate one of the directly:

```python
>>> from htmlelements.element import Element
>>> str(Element("Hello!"))
'<element>Hello!</element>'
```

This is because the element name is derived from the class name. Therefore:

```python
>>> from htmlelements.element import Element
>>> class Div(Element): ...
>>> str(Div("Hello!"))
'<div>Hello!</div>'
```

If you want to create a void element:

```python
>>> from htmlelements.element import VoidElement
>>> class Img(VoidElement): ...
>>> str(Img("this is ignored", "also ignored"), src="img.png")
'<img src="img.png">'
```

Both Element and VoidElement are convenience classes. All they do is remove the
need to pass the `_void` keyword parameter to BaseElement

```python
>>> from htmlelements.element import BaseElement
>>> class Img(BaseElement): ...
>>> str(Img("this is ignored", "also ignored"), src="img.png", _void=True)
'<img src="img.png">'
```

## Element Children

Any non-keyword parameter passed is added as children.

You can pass any object that has `__str__` implemented (and every Element
has `__str__`) or any callable that returns something that has `__str__`.

```python
>>> from htmlelements import P, Span
>>> str(P("Hello", "World", 1.0 ,Span('SpanSpam')))
'<p>HelloWorld1.0<span>SpanSpam</span></p>'
```

Note that the `'Hello'`, `'World` and `1.0` have no space between them. So it's
better to handle it before:

```python
>>> from htmlelements import P, Span
>>> s = " ".join(["Hello", "World", str(1.0)])
>>> str(P(s,Span('SpanSpam')))
'<p>Hello World 1.0<span>SpanSpam</span></p>'
```

## Element attributes

Any keyword parameter passed to the elements are added as attributes, with
some caveats:

- `_void` is used to control if the element should be a void element or not.
  This is only applicable when using `BaseElement` directly. `Element` and
  `VoidElement` import handle this parameter automatically
- `classes` gets converted to the attribute `class`. This is done because
  `class` is a python keyword and as such can't be used as a parameter
- `label_for` gets converted to the attribute `for`. Same reason as
  `classes/class`

As for the values themselves, any object that have `__str__` implemented is
fine, as well as any callable that returns a value with `__str__`.

```python
>>> from htmlelements import P
>>> l = [1, 2]
>>> str(P("Hello!", classes=l)
'<p class="[1, 2]">Hello!</p>'
```

```python
>>> from htmlelements import Img, P
>>> str(Div("Hello!"), classes="font-bold bg-white text-black")
'<div class="font-bold bg-white text-black">Hello</div>'
```

Exception for `True` and `False`. Those two values will be converted to the
strings `'true'` and `'false'`.

If you do no want to use keyword arguments a `dict` can be used instead:

```python
>>> from htmlelements import P
>>> attrs = {"class": "bg-white"}
>>> str(P("Hello!", **attrs))
'<p class="bg-white">Hello!</p>'
```

Using a dict this way allows you to use `class` and `for` directly.

## Building pages

Here's a simple mockup: a home page that lists articles, an article page
that shows a single article and an about page. All three using a
common template.

```python

from typing import NamedTuple

from htmlelements import H1, H2, A, Body, Div, Head, P, Title
from htmlelements.utils import html


class Article(NamedTuple):
    id: int
    title: str
    content: str


ARTICLES: list[Article] = [
    Article(1, "Article 1", "Lorem Ipsum"),
    Article(2, "Article 2", "Ipsum Lorem"),
]


def get_articles():
    return ARTICLES

def get_article(article_id: int):
    return next(a for a in ARTICLES if a.id == article_id)

def template(*content, page_title=""):
    return html(
        Head(Title(page_title or "A HTML Page")),
        Body(
            Div("Maybe the site navigation goes here"),
            H1("Welcome to this site!", classes="text-lg"),
            Div(
                *content,
                classes="mx-auto",
            ),
        ),
    )

def article(article_id: int):
    article = get_article(article_id)
    return template(
        H2(article.title),
        Div(
            *[P(paragraph) for paragraph in article.content.split("\n")],
        )
        page_title=article.title,
    )

def home():
    return template(
        *[H2(A(a.title, href=f"/{a.id}")) for a in get_articles()],
    )


def about():
    return template(
        P("Made with python!"),
    )


print(home())
print(article(1))
print(about())
```

## Using with Django

There's two ways: passing the elements to the django template or not using
django templates at all

### With Django's template

This works because Element objects have `__str__` and can be rendered in the
template with just `{{ var }}`

```html
<p>Just the contents of template.html</p>
{{ content }}
```

```python
from htmlelements import P
from django.shortcuts import render
from django.http import HttpRequest

def view(request: HttpRequest):
  context = {
    "content": P("Hello!")
  ]
  return render(request, "template.html", context)
```

### Without Django's template

```python
from htmlelements.utils import html
from htmlelements import P, Head, Body
from django.http import HttpRequest, HttpResponse

def view(request: HttpRequest):
  return HttpResponse(
    html(
      Head(),
      Body(
        P("Hello!")
      ),
    )
  )

```

### Django utilities

Some things in Django are commonly handled by context processors and so
depend on the template engine.

One of those things is CSRF tokens.

So there are two utilities in the `htmlelements.django` module to help with that.

#### csrf_token

Just a wrapper around `django.middleware.csrf.get_token` that returns a
function. Use as a callable to produce the token only when needed.

```python
from django.http import HttpRequest, HttpResponse

from htmlelements import Body, Form, Head
from htmlelements.django.csrf import csrf_token
from htmlelements.utils import html


def view(request: HttpRequest):
    return HttpResponse(
        html(
            Head(),
            Body(
                Form(
                    Input(
                        type="hidden",
                        value=csrf_token(request),
                        name="csrfmiddlewaretoken",
                    ),
                    method="POST",
                )
            ),
        )
    )
```

#### csrf_input

Given that you will most likely want to add the CSRF token as a hidden input, this
does just that.

The code above is equivalent to:

```python
from django.http import HttpRequest, HttpResponse

from htmlelements.django.csrf import csrf_input
from htmlelements import Body, Form, Head
from htmlelements.utils import html


def view(request: HttpRequest):
    return HttpResponse(
        html(
            Head(),
            Body(
                Form(
                    csrf_input(request),
                    method="POST",
                )
            ),
        )
    )

```
