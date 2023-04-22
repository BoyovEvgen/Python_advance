import re


def count_words():
    text = input('Input your text: ')
    word = input('Input your word: ')
    new_text, count = re.subn(r'\b{}\b'.format(word), word.upper(), text)
    print(new_text, f'\n number of matches - {count}')


count_words()
