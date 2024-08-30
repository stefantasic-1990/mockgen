import openai
import requests
import configparser
import os

## read-in configs
config = configparser.ConfigParser()
config.read("./config.ini")

api_key = config.get("OPENAI", "API_KEY")
endpoint = config.get("OPENAI", "ENDPOINT")
model = config.get("OPENAI", "MODEL")

temp_dir = config.get("MOCKGEN", "TEMP_DIR")

prompt = [{"role": "user", "content": "Give me three rows by three columns of mock CSV data, and do not give me any other text."}]

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": model,
    "messages": prompt
}

response = requests.post(endpoint, headers=headers, json=data)

if response.status_code == 200:
    response_json = response.json()
    response_text = response_json['choices'][0]['message']['content']
else:
    print(f"HTTP Error: {response.status_code}")

filename = f"{temp_dir}/data.csv"

if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

with open(filename, "w") as file:
    file.write(response_text.strip("`").strip())

def get_data():
    return

def load_data():
    return

