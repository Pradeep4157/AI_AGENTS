# 5 factors to make prompt secure : 
# 1) Role : Define the domain name and responsibility in that domain for the llm. Eg : Senior Software engineer for 
# reviewing codes.
# 2) Task : What's does the llm needs to do.
# 3) Constraints : Here we can define the categories in which the issue can be classified into.. 
# 4) Output Format : Here we define the format in which the llm needs to respond. Eg : JSON format
# 5) Zero Shot / One Shot / Few Shots: If we give 1 eg to llm then that's called One Shot and when we dont give any eg
#  that's called zero shot and if we give multiple examples to llm that's called few shots. Eg can be the type of question 
# and the way llm needs to respond. 
# 6) Fallback : If the query does not fit in any of the categories that  we have defined earlier, then we just return other. 

import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key: 
    raise ValueError("API key nhi milra")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-20b"

def llm_ans(prompt):
    message= {
        "role" : "user",
        "content" : prompt
    }
    messages = [message]
    response = client.chat.completions.create(model=model, messages=messages)
    ans=response.choices[0].message.content
    return ans

bad_prompt = """
#ROLE: 
You are a support assistant at a mobile / laptop company
#TASK: 
You have to classify the issue in a category
#CONSTRAINT: 
You have to classify the issue in 1 of the 3 categories namely billing, technical, return
#OUTPUT FORMAT: 
Your answer should be in one word only. The one word should be one of the categories given in constraints.
#EXAMPLE:
For instance if the user complaint says he want refund the category is Return
#FALLBACK:
if the issue is unrelated to any of the issues mentioned in constraints, then the answer should be OTHER.
This is a user complaint : My laptop is not working
"""

print(llm_ans(bad_prompt))