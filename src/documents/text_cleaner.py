import re


def clean_text(text):
    # fix words broken across lines like "safe-\nty"
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)

    # remove extra spaces
    text = re.sub(r'[ \t]+', ' ', text)

    # remove lines that are just page numbers
    text = re.sub(r'(?m)^\s*\d+\s*$', '', text)

    # remove too many blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    text = text.strip()
    return text


def get_word_count(text):
    return len(text.split())


# test
if __name__ == "__main__":
    sample = """
    1

    Safety Proce-
    dures Manual

    All employees must follow these   rules at all times.

    2
    """

    cleaned = clean_text(sample)
    print("Cleaned text:")
    print(cleaned)
    print("Word count:", get_word_count(cleaned))
