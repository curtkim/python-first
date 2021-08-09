from pygments.token import Token
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import PygmentsTokens

text = [
    (Token.Keyword, 'print'),
    (Token.Punctuation, '('),
    (Token.Literal.String.Double, '"'),
    (Token.Literal.String.Double, 'hello'),
    (Token.Literal.String.Double, '"'),
    (Token.Punctuation, ')'),
    (Token.Text, '\n'),
]

print_formatted_text(PygmentsTokens(text))

