from functional_programming.decorators.markdown_to_text import markdown_to_text_decorator


@markdown_to_text_decorator
def concat(first_doc: str, second_doc: str) -> str:
    return f"""  First: {first_doc}
  Second: {second_doc}"""


@markdown_to_text_decorator
def format_as_essay(title: str, body: str, conclusion: str) -> str:
    return f"""  Title: {title}
  Body: {body}
  Conclusion: {conclusion}"""