import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from groq import Groq
from pydantic import BaseModel
from pathlib import Path
from pypdf import PdfReader

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key: 
    raise ValueError("api key nhi milra..")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-20b"


app = FastAPI()

@app.get("/")
def home():
    resume_text = read_pdf(Path("Pradeep_AM.pdf"))

    return {
        "message" : "HireMeAI is running",
        "Resume Content": resume_text
    }

# Pdf Extraction

def read_pdf(file_path : Path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text



def parse_resume(resume_text):
    system_prompt = """
    You are an expert resume parser.

    Extract information from the resume based on its meaning,
    not only based on exact section headings.

    Different resumes may use different headings.

    For example:
    - "Professional Experience" and "Work History" mean the same thing.
    - "Technical Expertise" and "Skills" mean the same thing.
    - "Academic Background" and "Education" mean the same thing.
    - "Selected Projects" and "Personal Projects" mean the same thing.

    Extract the following information:

    1. Personal Information:
       - Full name
       - Email
       - Phone
       - Location
       - LinkedIn URL
       - GitHub URL
       - Portfolio URL

    2. Professional Summary

    3. Education:
       - Institution
       - Degree
       - Field of study
       - Start date
       - End date
       - CGPA or percentage

    4. Work Experience:
       - Company
       - Job title
       - Start date
       - End date
       - Responsibilities
       - Achievements
       - Technologies used

    5. Projects:
       - Project name
       - Description
       - Technologies used
       - GitHub URL
       - Live deployment URL

    6. Technical Skills:
       - Programming languages
       - Frameworks and libraries
       - Databases
       - Developer tools
       - Other technical skills

    7. Achievements:
       - Description
       - Date
       - Associated URL

    8. Certifications:
       - Name
       - Issuing organization
       - Date

    IMPORTANT RULES:

    - Extract information based on context and meaning.
    - Do not invent or assume missing information.
    - Use null for missing individual values.
    - Use empty arrays for missing collections.
    - Preserve the original meaning of descriptions.
    - Extract URLs wherever they are available in the text.
    - Do not confuse projects with professional experience.
    - Return valid JSON only. No Markdown or additional explanation.

    Expected JSON structure:

    {
        "personal_info": {
            "name": null,
            "email": null,
            "phone": null,
            "location": null,
            "linkedin": null,
            "github": null,
            "portfolio": null
        },
        "summary": null,
        "education": [],
        "experience": [],
        "projects": [],
        "skills": {
            "languages": [],
            "frameworks": [],
            "databases": [],
            "tools": [],
            "other": []
        },
        "achievements": [],
        "certifications": []
    }
    """

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"Parse the following resume:\n\n{resume_text}"
            }
        ],
        response_format={"type": "json_object"}
    )

    response_text = completion.choices[0].message.content
    

    return json.loads(response_text)
