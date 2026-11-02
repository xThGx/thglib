from enum import Enum


class DocFormat(Enum):
    PDF = 1
    TXT = 2
    MD = 3
    HTML = 4


# Don't touch above this line


def convert_format(
    content: str, from_format: DocFormat, to_format: DocFormat | None
) -> str:
    match(from_format, to_format):
        case (DocFormat.MD, DocFormat.HTML):
            return f"{content.replace("# ", "<h1>")}</h1>"
        case (DocFormat.TXT, DocFormat.PDF):
            return f"[PDF] {content} [PDF]"
        case (DocFormat.HTML, DocFormat.MD):
            return f"{content.replace("<h1>", "# ").replace("</h1>", "")}"
        case _:
            raise Exception("invalid type")

            
# Test um zu sehen was ausgegeben wird
'''
x = DocFormat.TXT
print(x.HTML)
print(DocFormat.TXT)
print(DocFormat.TXT.value)
print(DocFormat.TXT.name)
print(DocFormat.TXT == 2)
'''

content = "Something wicked"
from_format = DocFormat.TXT
# from_format = None
to_format = None

print(convert_format(content, from_format, to_format))
