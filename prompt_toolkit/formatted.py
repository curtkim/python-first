from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

# The text.
text = FormattedText([
    ('class:aaa', 'Hello'),
    ('', ' '),
    ('class:bbb', 'World'),
])

# The style sheet.
style = Style.from_dict({
    'aaa': '#ff0066',
    'bbb': '#44ff00 italic',
})

print_formatted_text(text, style=style)


