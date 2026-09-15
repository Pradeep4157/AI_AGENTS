# Prompt Chaining : Here we break the whole prompt (whole task) in small prompts and pass the output of one 
# prompt to the next prompt. 
# Reasons to use : 
# 1) Debugging : If we use the whole big prompt instead of small prompts, it will be really difficult to identify which all 
# steps caused the error. 
# 2) Modularity : Incase some error is caused since the process is separated, only small changes in some functions are needed.
# 3) Different Models : Instead of making some complex model do all the complex as well as easy tasks, we can assign 
#  complex tasks to good models whereas simple tasks to some cheap model. 
# 4) Retry Steps : Incase some step failed we can add retries at that step. 
# How is it different from ReAct : 
# In ReAct the llm itself decides the tools that are required for some x step and on the basis of output, llm decides 
# the next steps as well whereas in Prompt Chaining we decide what the whole process is going to be. 

import os
from dotenv import load_dotenv
from groq import Groq
from time import sleep

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key: 
    raise ValueError("api key nhi milra..")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-20b"

JD = """
We are hiring Backend Python Developer

Requirements: 
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- Rest APIs
- 2+ years of experience
"""

RESUME= """
Name: Rahul Sharma

Experience: 
3 years as a Software Developer

Skills: 
Python, FastAPI, MySQL, Docker, Rest API's, Git 

Projects: 
Build a food delivery backend using 
FastAPI and MySQL

Deployed Application using Docker. 
"""

def ask_llm(system_prompt, user_prompt):
    system_message = {
        "role": "system",
        "content" : system_prompt
    }
    user_message = {
        "role" : "user",
        "content" : user_prompt
    }
    messages = [system_message, user_message]
    response = client.chat.completions.create(model = model, messages = messages)
    answer = response.choices[0].message.content
    return answer

def step_1_skills_extraction(): 
    system_prompt = """You are a professional HR assistant. Extract the skills from the candidates resume provided. 
    Only Return  the skills, nothing else. Do not invent any skills yourself."""

    user_prompt = f"""Extract the skills from this resume. {RESUME}"""

    return ask_llm(system_prompt, user_prompt)

def step_2_JD_extract(): 
    system_prompt = """You are a professional HR assistant. Extract the skills from the Job Description provided. 
    Only Return  the skills, nothing else. Do not invent any skills yourself."""

    user_prompt = f"""Extract the skills from this Job Description. {JD}"""

    return ask_llm(system_prompt, user_prompt)

def step_3_skills_match(candidate, jd):
    system_prompt = """ You are a professional HR assistant. Compare the skills of candidate and skills required in the JD
    and provide a final score between 1 and 100. Also give a verdict whether the candidate is a good fit for the role.
    """
    user_prompt = f"""Compare and match the skills
    JD : {jd} 
    Candidate : {candidate} """
    return ask_llm(system_prompt, user_prompt)

candidate = step_1_skills_extraction()
sleep(2)
jd = step_2_JD_extract()
sleep(3)
score = step_3_skills_match(candidate, jd)
print(score)
