



import os
import openai

def o1(inputs, system_prompt):
    api_key = os.environ["OPENAI_API_KEY"]
    engine = openai.OpenAI(api_key=api_key)
    response = engine.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "user", "content": system_prompt + "\n\n" + inputs}
        ],
    )
    return response.choices[0].message.content


prompt = "How many cms is 1 feet"
system_prompt = "You are a civil engineer."

print(o1(prompt, system_prompt))

# import os, requests
# key = os.environ["OPENAI_API_KEY"]
# r = requests.get("https://api.openai.com/v1/models",
#                  headers={"Authorization": f"Bearer {key}"})
# # print(r.status_code)
# # print(r.json())

# models = r.json().get("data", [])
# available_models = {m["id"] for m in models}
# if "gpt-4o-2024-08-06" in available_models:
#     print("yes!")
# else:
#     print(available_models)
