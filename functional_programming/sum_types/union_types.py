class Parsed:
    def __init__(self, doc_name: str, text: str) -> None:
        self.doc_name = doc_name
        self.text = text


class ParseError:
    def __init__(self, doc_name: str, err: str) -> None:
        self.doc_name = doc_name
        self.err = err


# Don't touch above this line


def parse_document(doc_name: str, content: str) -> Parsed | ParseError:
    if content:
        return Parsed(doc_name, content)
    return ParseError(doc_name, err="no content")


def display_parse_result(result: Parsed | ParseError) -> str:
    if isinstance(result, Parsed):
        return f"Parsed {result.doc_name}: {len(result.text)} characters"
    if isinstance(result, ParseError):
        return f"Failed {result.doc_name}: {result.err}"
        