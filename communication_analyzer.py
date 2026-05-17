import language_tool_python


tool = language_tool_python.LanguageTool('en-US')


def analyze_communication(text):

    matches = tool.check(text)

    mistakes = []

    ignore_words = [
        "Possible spelling mistake found",
        "too many consecutive spaces",
        "repeated a whitespace"
    ]


    for match in matches[:10]:

        message = match.message

        # skip useless resume warnings
        if any(word.lower() in message.lower() for word in ignore_words):
            continue

        mistakes.append({

            "message": message,

            "incorrect": text[
                match.offset :
                match.offset + match.error_length
            ]
        })


    # better scoring
    score = max(100 - (len(mistakes) * 5), 0)

    return mistakes, score