from typing import Generator
from bs4 import BeautifulSoup

MAX_LEN = 4096


class FragmentTooLargeError(Exception):
    def __init__(self, element, max_len):
        super().__init__(f"Element too large to fit within max_len ({max_len} chars): {element[:100]}...")


def split_message(source: str, max_len: int = MAX_LEN) -> Generator[str, None, None]:
    soup = BeautifulSoup(source, "html.parser")
    elements = soup.body.contents if soup.body else soup.contents

    current_fragment = []
    current_length = 0

    for element in elements:
        element_html = str(element)
        element_length = len(element_html)

        closing_tags_length = len(_get_closing_tags(current_fragment)) if current_fragment else 0

        if element_length > max_len:
            for part in _split_large_element(element_html, max_len):
                if current_length + len(part) + closing_tags_length > max_len:
                    yield _ensure_valid_html("".join(current_fragment))
                    current_fragment = []
                    current_length = 0
                current_fragment.append(part)
                current_length += len(part)
        elif current_length + element_length + closing_tags_length > max_len:
            yield _ensure_valid_html("".join(current_fragment))
            current_fragment = [element_html]
            current_length = element_length
        else:
            current_fragment.append(element_html)
            current_length += element_length

    if current_fragment:
        yield _ensure_valid_html("".join(current_fragment))


def _split_large_element(element_html: str, max_len: int) -> Generator[str, None, None]:
    soup = BeautifulSoup(element_html, "html.parser")
    if len(str(soup)) <= max_len:
        yield element_html
        return

    stack = [soup]
    current_fragment = []
    current_length = 0

    while stack:
        element = stack.pop()
        for content in reversed(element.contents):
            content_html = str(content)
            content_length = len(content_html)

            if content_length > max_len:
                if content.name is None:
                    text_parts = _split_text_content(content_html, max_len)
                    for part in text_parts:
                        if current_length + len(part) > max_len:
                            yield _ensure_valid_html("".join(current_fragment))
                            current_fragment = []
                            current_length = 0
                        current_fragment.append(part)
                        current_length += len(part)
                else:
                    stack.append(BeautifulSoup(content_html, "html.parser"))
            else:
                if current_length + content_length > max_len:
                    yield _ensure_valid_html("".join(current_fragment))
                    current_fragment = []
                    current_length = 0
                current_fragment.append(content_html)
                current_length += content_length

    if current_fragment:
        yield _ensure_valid_html("".join(current_fragment))


def _split_text_content(content: str, max_len: int) -> list:
    return [content[i:i + max_len] for i in range(0, len(content), max_len)]


def _get_closing_tags(elements: list) -> str:
    soup = BeautifulSoup("".join(elements), "html.parser")
    closing_tags = [f"</{tag.name}>" for tag in reversed(soup.find_all()) if tag.name]
    return "".join(closing_tags)


def _ensure_valid_html(fragment: str) -> str:
    soup = BeautifulSoup(fragment, "html.parser")
    return str(soup)
