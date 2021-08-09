from prompt_toolkit.shortcuts import input_dialog

text = input_dialog(
    title='Input dialog example',
    text='Please type your name:').run()

