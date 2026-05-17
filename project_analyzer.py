import re


def analyze_projects(text):

    text_lower = text.lower()

    technologies = {

        "python": "Python",
        "flask": "Flask",
        "html": "HTML",
        "css": "CSS",
        "javascript": "JavaScript",
        "mysql": "MySQL",
        "sql": "SQL",
        "machine learning": "Machine Learning",
        "java": "Java",
        "react": "React",
        "node": "Node.js",
        "docker": "Docker"
    }


    # detect project section
    project_patterns = [

        r'projects?(.*?)(education|skills|certifications|$)',

        r'training & projects(.*?)(education|skills|certifications|$)'
    ]


    project_text = ""

    for pattern in project_patterns:

        match = re.search(
            pattern,
            text_lower,
            re.DOTALL
        )

        if match:

            project_text = match.group(1)
            break


    used_tech = []

    for key, value in technologies.items():

        if key in project_text:

            used_tech.append(value)


    suggestions = []


    # quality checks
    if len(project_text.strip()) < 30:

        suggestions.append(
            "Project section is too small"
        )

        suggestions.append(
            "Add detailed project descriptions"
        )

    else:

        suggestions.append(
            "Good project section detected"
        )


    if len(used_tech) < 2:

        suggestions.append(
            "Mention technologies used in projects"
        )


    if "github" not in project_text:

        suggestions.append(
            "Add GitHub links for projects"
        )


    if "http" not in project_text:

        suggestions.append(
            "Add deployed/live project links"
        )


    if not project_text:

        suggestions.append(
            "No project section detected"
        )

        suggestions.append(
            "Add at least 2 strong projects"
        )


    return used_tech, suggestions