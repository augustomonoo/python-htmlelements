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
        ),
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
