# Currying Practice

Markdown makes [displaying images](https://www.markdownguide.org/basic-syntax/#images-1) as simple as possible. To add an image to a Markdown document, just use this syntax:

```Text
![alt text](url "title")
```

`alt text`: a brief description for screen readers and web scrapers; required for accessibility.
`url`: a URL or relative path to the image.
`title`: shown on mouse hover; optional.

## Assignment

Doc2Doc makes using markdown a breeze. This includes adding images to markdown documents.
**Complete the `create_markdown_image` function** using currying. It takes a string input, `alt_text`.

- [ ] Enclose the `alt_text` in square brackets prefixed with an exclamation point: `![alt_text]`
- [ ] Define an inner function that also takes a string input, `url`:
  - [ ] The inner function should first [escape](https://en.wikipedia.org/wiki/Escape_sequence) any parentheses in the URL by replacing them with [encoded sequences](https://www.url-encode-decode.com/).
    - [ ] Use the `.replace()` string method to change any opening parenthesis `(` into `%28`.
    - [ ] Do the same to change any closing parenthesis `)` into `%29`.
  - [ ] Enclose the `url` with parentheses: `(url)`
  - [ ] Add the enclosed `url` to the end of the enclosed `alt_text`: `![alt_text](url)`
  - [ ] Define the innermost function. It should take an optional string input for the `title` (`title=None`).
    - [ ] If a `title` is passed:
      - [ ] Enclose it in double quotes.
      - [ ] Add the quoted `title` to the image syntax by first removing the closing parenthesis `)` from the end of the image syntax.
            Add a space and the quoted `title` with a closing parenthesis `)` to the end of the image syntax: `![alt_text](url "title")`
    - [ ] Return the finished image syntax.
  - [ ] Return the innermost function.

- [ ] Return the inner function.
