class MaybeParsed:
    pass


# Don't touch above this line

# Task
'''
class Parsed(MaybeParsed):
    def __init__(self, doc_name: str, text: str) -> None:
        pass


class ParseError(MaybeParsed):
    def __init__(self, doc_name: str, err: str) -> None:
        pass
'''

# -------------------------------------------------------------------

# Result
class Parsed(MaybeParsed):
    def __init__(self, doc_name: str, text: str) -> None:
        self.doc_name = doc_name
        self.text = text


class ParseError(MaybeParsed):
    def __init__(self, doc_name: str, err: str) -> None:
        self.doc_name = doc_name
        self.err = err
