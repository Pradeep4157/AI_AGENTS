# Instead of getting whole response at once, it streams / sends the response in chunks. 
import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key: 
    raise ValueError("api key nhi milra..")

client = Groq(api_key = my_api_key)
model = "openai/gpt-oss-20b"
prompt = "Explain how internet works"
message = {
    "role" : "user",
    "content" : prompt
}
messages = [message]
stream = client.chat.completions.create(model = model, messages = messages, stream=True)
for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content,end="",flush=True)
        