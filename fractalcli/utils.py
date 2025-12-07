import re


def strip_ansi(text):
    ansi_escape = re.compile(r'\\x1b\[.*?m')
    return re.sub(ansi_escape, '', text)
