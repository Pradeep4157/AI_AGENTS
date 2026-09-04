#  Tokenisation : llm breaks the input into smaller words or subwords whose meaning is known by it, this process
# of breaking input into smaller word or subwords is called tokenisation and these smallest unit in which it breaks the 
# input (word / subword) is called a token.
import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key nhi milra isse")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-20b"
role="user"
prompt_1 = "Hi!"
prompt_2 = "Explain time travel in detail"
prompt_3 = "Write a 1000 words essay on machine learning"

prompts = [prompt_1, prompt_2, prompt_3]

for prompt in prompts:
    message = {
        "role" : role,
        "content" : prompt,
    }
    messages = [message]
    response = client.chat.completions.create(model=model, messages=messages, max_tokens = 50)
    usage=response.usage
    print(f"Prompt: {prompt} --> your tokens : {usage.prompt_tokens} completion_tokens: {usage.completion_tokens} and total tokens : {usage.total_tokens} finish Reason : {response.choices[0].finish_reason}")

