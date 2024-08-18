# import os
# import openai
# from config import apikey
#
# # Set the API key
# openai.api_key = apikey
#
# # Create a chat completion using the new model
# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo-instruct",  # You can also use "gpt-4" if available
#     messages=[
#         {"role": "user", "content": "Write an email to my boss for resignation?"}
#     ],
#     temperature=0.7,
#     max_tokens=256,
#     top_p=1,
#     frequency_penalty=0,
#     presence_penalty=0
# )
#
# # Print the response from the API
# print(response['choices'][0]['message']['content'])


from groq import Groq
from config import apikey

# Initialize the Groq client with your API key
client = Groq(api_key=apikey)

# Create a chat completion request
completion = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "user",
            "content": "write an email to my boss for my resignation\n"
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

# Stream the completion result
for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
