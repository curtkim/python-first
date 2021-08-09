from pygments.lexers.html import HtmlLexer
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.lexers import PygmentsLexer

text = prompt('Enter HTML: ', lexer=PygmentsLexer(HtmlLexer))
print('You said: %s' % text)


