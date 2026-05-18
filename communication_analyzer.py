def analyze_communication(text):

    suggestions = []

    score = 100

    lines = text.splitlines()

    for line in lines:

        if len(line.strip()) > 120:

            suggestions.append({

                "incorrect": line[:40],

                "message": "Sentence is too long. Try making it shorter."

            })

            score -= 5


    if "team leadership" in text.lower():

        suggestions.append({

            "incorrect": "Team Leadership",

            "message": "Good leadership skill mentioned."

        })


    if "communication" in text.lower():

        suggestions.append({

            "incorrect": "Communication",

            "message": "Good communication skill detected."

        })


    if score < 0:
        score = 0

    return suggestions, score