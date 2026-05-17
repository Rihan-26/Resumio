from communication_analyzer import analyze_communication
from project_analyzer import analyze_projects
from project_analyzer import analyze_projects
from flask import Flask, render_template, request
import os

from resume_parser import (
    extract_text_from_pdf,
    extract_text_from_docx
)

from skill_matcher import (
    extract_skills,
    match_role
)

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# create uploads folder automatically
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():

    if 'resume' not in request.files:
        return "No file uploaded"

    file = request.files['resume']

    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        file.filename
    )

    file.save(filepath)

    role = request.form['role']

    extracted_text = ""

    # extract text
    if file.filename.endswith('.pdf'):

        extracted_text = extract_text_from_pdf(filepath)

    elif file.filename.endswith('.docx'):

        extracted_text = extract_text_from_docx(filepath)

    else:
        return "Unsupported file format"


    # detect skills
    found_skills = extract_skills(extracted_text)

    mistakes, communication_score = analyze_communication(
        extracted_text
    )
    used_tech, project_suggestions = analyze_projects(
    extracted_text
)


    # soft skills list
    soft_skills_list = [

        "leadership",
        "team leadership",
        "communication",
        "decision making",
        "teamwork",
        "speaking",
        "writing skills",
        "speaking and writing skills",
        "problem solving",
        "time management"
    ]


    # separate technical and soft skills
    soft_skills = []
    technical_skills = []


    for skill in found_skills:

        if skill in soft_skills_list:

            soft_skills.append(skill)

        else:

            technical_skills.append(skill)


    # role matching
    (
        matched_beginner,
        missing_beginner,

        matched_intermediate,
        missing_intermediate,

        matched_advanced,
        missing_advanced,

        match_score

    ) = match_role(found_skills, role)


    # soft skills score
    soft_score = len(soft_skills) * 15

    if soft_score > 100:
        soft_score = 100


    # profile level
    if match_score < 30:

        level = "Beginner 🚀"

    elif match_score < 60:

        level = "Intermediate 👍"

    else:

        level = "Strong Profile 🔥"


    return f"""

<!DOCTYPE html>
<html>

<head>

    <title>AI Resume Analyzer</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <style>

        *{{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body{{
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #020617, #0f172a, #1e293b);
            color: white;
            padding: 30px;
        }}

        .container{{
            width: 90%;
            margin: auto;
        }}

        .hero{{
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            padding: 35px;
            border-radius: 25px;
            margin-bottom: 25px;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.4);
        }}

        .hero h1{{
            font-size: 40px;
            margin-bottom: 10px;
        }}

        .hero p{{
            opacity: 0.9;
            font-size: 18px;
        }}

        .stats{{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }}

        .card{{
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(10px);
            padding: 25px;
            border-radius: 20px;
        }}

        .score{{
            font-size: 35px;
            font-weight: bold;
        }}

        .skills-grid{{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }}

        .skill-box{{
            background: rgba(255,255,255,0.08);
            padding: 25px;
            border-radius: 20px;
        }}

        .badge{{
            display: inline-block;
            padding: 10px 16px;
            border-radius: 30px;
            margin: 8px;
            font-size: 14px;
            font-weight: 500;
        }}

        .tech{{
            background: #2563eb;
        }}

        .soft{{
            background: #7c3aed;
        }}

        .good{{
            background: #16a34a;
        }}

        .missing{{
            background: #dc2626;
        }}

        .learning{{
            background: #f59e0b;
            color: black;
        }}

        .section{{
            background: rgba(255,255,255,0.08);
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 25px;
        }}

        .section h2{{
            margin-bottom: 20px;
        }}

        .resume-box{{
            background: #0f172a;
            padding: 25px;
            border-radius: 15px;
            max-height: 500px;
            overflow-y: auto;
            white-space: pre-wrap;
            line-height: 1.7;
        }}

        .progress{{
            width: 100%;
            height: 18px;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            overflow: hidden;
            margin-top: 15px;
        }}

        .progress-bar{{
            height: 100%;
            background: linear-gradient(90deg, #22c55e, #3b82f6);
            width: {match_score}%;
        }}

    </style>

</head>

<body>

    <div class="container">

        <div class="hero">

    <h1>🚀 AI Resume Analyzer</h1>

    <p>Smart Career Advisor using AI + NLP</p>

    <div class="creator">

        <h3>Developed By</h3>

        <h2>C S Rihan</h2>

        <p>📧 rihanshaik855@gmail.com</p>

    </div>

</div>


        <div class="stats">

            <div class="card">

                <h2>🎯 Target Role</h2>

                <div class="score">{role}</div>

            </div>


            <div class="card">

                <h2>🧑‍💻  Technical Score</h2>

                <div class="score">{match_score}%</div>

                <div class="progress">

                    <div class="progress-bar"></div>

                </div>

            </div>


            <div class="card">

                <h2>🤝 Soft Skills</h2>

                <div class="score">{soft_score}%</div>

            </div>


            <div class="card">

                <h2>🗣️ Communication</h2>

                <div class="score">{communication_score}%</div>

            </div>

        </div>


        <div class="skills-grid">

            <div class="skill-box">

                <h2>💻 Technical Skills</h2>

                {
                    ''.join(
                        f'<span class="badge tech">{skill}</span>'
                        for skill in technical_skills
                    )
                }

            </div>


            <div class="skill-box">

                <h2>🤝 Soft Skills</h2>

                {
                    ''.join(
                        f'<span class="badge soft">{skill}</span>'
                        for skill in soft_skills
                    )
                }

            </div>

        </div>


        <div class="section">

            <h2>🔥 Profile Level: {level}</h2>

        </div>


        <div class="section">

            <h2>✅ Beginner Skills You Have</h2>

            {
                ''.join(
                    f'<span class="badge good">{skill}</span>'
                    for skill in matched_beginner
                )
            }

        </div>


        <div class="section">

            <h2>📘 Recommended Beginner Skills</h2>

            {
                ''.join(
                    f'<span class="badge missing">{skill}</span>'
                    for skill in missing_beginner
                )
            }

        </div>


        <div class="section">

            <h2>📈 Intermediate Skills To Learn</h2>

            {
                ''.join(
                    f'<span class="badge learning">{skill}</span>'
                    for skill in missing_intermediate
                )
            }

        </div>


        <div class="section">

            <h2>🚀 Advanced Skills For Future</h2>

            <ul>

                {
                    ''.join(
                        f'<li>{skill}</li>'
                        for skill in missing_advanced
                    )
                }

            </ul>

        </div>


        <div class="section">

            <h2>📝 Communication Suggestions</h2>

            <ul>

                {
                    ''.join(
                        f'<li><b>{m["incorrect"]}</b> → {m["message"]}</li>'
                        for m in mistakes
                    )
                }

            </ul>

        </div>
        <div class="section">

    <h2>🚀 Project Technologies Detected</h2>

    {
        ''.join(
            f'<span class="badge tech">{tech}</span>'
            for tech in used_tech
        )
    }

</div>


<div class="section">

    <h2>📌 Project Suggestions</h2>

    <ul>

        {
            ''.join(
                f'<li>{tip}</li>'
                for tip in project_suggestions
            )
        }

    </ul>

</div>


        <div class="section">

            <h2>📄 Extracted Resume Text</h2>

            <div class="resume-box">

                {extracted_text}

            </div>

        </div>

    </div>

</body>

</html>

"""


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)