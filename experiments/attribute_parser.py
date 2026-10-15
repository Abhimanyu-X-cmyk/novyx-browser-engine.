
from html.parser import HTMLParser


class Element:
    def __init__(self, tag, attrs=None, text=""):
        self.tag = tag
        self.attrs = dict(attrs or [])
        self.text = text
        self.children = []

    def display(self, depth=0):
        indent = "  " * depth
        details = ""

        if self.attrs:
            details = " " + str(self.attrs)

        print(indent + self.tag + details)

        if self.text:
            print(indent + "  " + self.text)

        for child in self.children:
            child.display(depth + 1)


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
            text_node = Element("#text", text=data.strip())
            self.stack[-1].children.append(text_node)


def main():
    html = """
    <div id="main">
        <h1>NOVYX Browser Engine</h1>
        <img src="logo.png" alt="NOVYX logo">
        <p class="intro">Our browser engine starts here.</p>
    </div>
    """

    parser = NOVYXParser()
    parser.feed(html)

    print("=== NOVYX Document Tree ===")
    parser.root.display()

    div = parser.root.children[0]
    heading = div.children[0]
    image = div.children[1]
    paragraph = div.children[2]

    assert div.tag == "div"
    assert div.attrs["id"] == "main"
    assert heading.tag == "h1"
    assert heading.children[0].text == "NOVYX Browser Engine"
    assert image.attrs["src"] == "logo.png"
    assert image.attrs["alt"] == "NOVYX logo"
    assert paragraph.attrs["class"] == "intro"
    assert paragraph.children[0].text == "Our browser engine starts here."

    print("\nAll 8 tests passed!")


if __name__ == "__main__":
    main()
