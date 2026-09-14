# ReAct : Reasoning + Action, llm reasons about the query and chooses the action (which tool to use or no tool call is needed) 
# according to the needs
# tools are just functions that we define .. 
import os
import re
from dotenv import load_dotenv
from groq import Groq
from time import sleep
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key: 
    raise ValueError("api key nhi milra..")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-20b"

#tools.. 

def get_product_price(product):
    if product == 'iPhone 17':
        return 1000
    elif product == 'iPhone 15':
        return 500
    else:
        return 0

def calculator(expression):
    try:
        return eval(expression)
    except:
        return "calc error!"
tools = {
    "get_product_price" : get_product_price,
    "calculator" : calculator
}

system_prompt = """
You are a shopping assistant.
You have these tools:
get_product_price(product) 
calculator(expression)
IMPORTANT:
call tools exactly like these examples:
Action : get_product_price("iPhone 17")
Action : calculator("5000 - 1000")

Never write: 
get_product_price(product = "iPhone 17")

Never write: 
calculator(expression="5000 - 1000")

Follow these rules: 

1. Decide what you need to do next. 
2. Call only one tool at a time. 
3. After writing an Action, STOP immediately. 
4. Never guess or invent a tool result. 
5. Wait until you recieve an observation. 
6. Then decide your next action. 
7. When the task is complete, give the Final Answer. 

Format: 

Thought : what you need to do. 
Action : tool_name(argument)

When finished: 

Final Answer : your answer 
"""

def run_agent(question):
    messages = [
        {
            "role" : "system",
            "content" : system_prompt
        },
        {
            "role" : "user",
            "content" : question
        }

    ]
    for step in range(5):
        print("\n------------------------------")
        print("Step", step + 1)
        print("--------------------------------")

        response = client.chat.completions.create(
            model = "llama-3.3-70b-versatile",
            messages = messages,
            temperature = 0,
            
        )
        answer = response.choices[0].message.content

        print(answer)

        if "Final Answer" in answer:
            break

        match = re.search(
            r"Action:\s*\*(\w+)\*\((.*?)\)",
            answer
        )

        if match: 
            tool_name = match.group(1)
            tool_input = match.group(2)
            tool_input = tool_input.strip()
            tool_input = tool_input.strip('"')

            if tool_name in tools: 
                tool = tools[tool_name]
                observation = tool(tool_input)

            else: 
                observation = "tool not found"

            print("Observation : ", observation)

            messages.append(
                {
                    "role" : "assistant",
                    "content" : answer
                }
            )
            messages.append(
                {
                    "role" : "user",
                    "content" : "Observation " + str(observation)
                }
            )
            sleep(5)



        


prompt = """
I have 5000 rupees. What is the price of an Iphone 17?
and how much money will i have left?"""

run_agent(prompt)