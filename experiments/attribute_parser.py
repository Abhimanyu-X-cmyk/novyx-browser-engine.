
from html.parser import HTMLParser


class Element:
    def __init__(self, tag, attrs=None, text=""):
        self.tag = tag
        self.attrs = dict(attrs or [])
        self.text = text
        self.children = []


class NOVYXParser(HTMLParser):
    VOID_TAGS = {
        "area", "base", "br", "col", "embed",
        "hr", "img", "input", "link", "meta",
        "source", "track", "wbr"
    }

    def __init__(self):
        super().__init__()
        self.root = Element("document")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        element = Element(tag, attrs)
        self.stack[-1].children.append(element)

        if tag not in self.VOID_TAGS:
            self.stack.append(element)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]
                break

    def handle_data(self, data):
        if data.strip():
            self.stack[-1].children.append(
                Element("#text", text=data.strip())
            )


if __name__ == "__main__":
    html = """
    <div id="main">
        <img src="logo.png" alt="NOVYX logo">
        <p class="intro">Welcome to NOVYX</p>
    </div>
    """

    parser = NOVYXParser()
    parser.feed(html)

    div = parser.root.children[0]
    img = div.children[0]
    paragraph = div.children[1]

    assert div.attrs["id"] == "main"
    assert img.attrs["src"] == "logo.png"
    assert img.attrs["alt"] == "NOVYX logo"
    assert paragraph.attrs["class"] == "intro"
    assert paragraph.children[0].text == "Welcome to NOVYX"

    print("All 5 attribute tests passed!")
