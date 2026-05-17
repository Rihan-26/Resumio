import csv
import re

from roles import roles


skills_db = {}


# load skills
with open("skills.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        skills_db[row['skill']] = int(row['weight'])


# extract skills from resume
def extract_skills(resume_text):

    resume_text = resume_text.lower()

    found_skills = []

    for skill in skills_db:

        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, resume_text):

            found_skills.append(skill)

    return found_skills


# role matching
def match_role(found_skills, target_role):

    role_data = roles[target_role]

    beginner = role_data["beginner"]
    intermediate = role_data["intermediate"]
    advanced = role_data["advanced"]

    matched_beginner = []
    missing_beginner = []

    matched_intermediate = []
    missing_intermediate = []

    matched_advanced = []
    missing_advanced = []


    # beginner
    for skill in beginner:

        if skill in found_skills:

            matched_beginner.append(skill)

        else:

            missing_beginner.append(skill)


    # intermediate
    for skill in intermediate:

        if skill in found_skills:

            matched_intermediate.append(skill)

        else:

            missing_intermediate.append(skill)


    # advanced
    for skill in advanced:

        if skill in found_skills:

            matched_advanced.append(skill)

        else:

            missing_advanced.append(skill)


    total_required = (
        len(beginner) +
        len(intermediate) +
        len(advanced)
    )

    total_found = (
        len(matched_beginner) +
        len(matched_intermediate) +
        len(matched_advanced)
    )

    match_score = int(
        (total_found / total_required) * 100
    )

    return (
        matched_beginner,
        missing_beginner,

        matched_intermediate,
        missing_intermediate,

        matched_advanced,
        missing_advanced,

        match_score
    )