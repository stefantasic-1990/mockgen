import requests
import configparser
import os
from requests.exceptions import HTTPError, RequestException

## read-in config
config = configparser.ConfigParser()
config.read("./config.ini")

## read-in input CSV


## get configs
api_key = config.get("OPENAI", "API_KEY")
endpoint = config.get("OPENAI", "ENDPOINT")
model = config.get("OPENAI", "MODEL")
tmp_dir = config.get("MOCKGEN", "TMP_DIR")

prompt = [{"role": "user", "content": "Give me three rows by three columns of mock CSV data, and do not give me any other text. Three tables. Table names are A, B, C, include separately inside CSV before the data."}]

def download_data(prompt):

    filename = f"{tmp_dir}/data.csv"

    ## request headers and data payload
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": prompt
    }

    ## send API request, extract andresponse content
    response = requests.post(endpoint, headers=headers, json=data)
    response.raise_for_status()

    if response.status_code == 200:
        response_text = response.json()['choices'][0]['message']['content']
    else:
        raise HTTPError(f"Server returned code {response.status_code}") 

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    with open(filename, "w") as file:
        file.write(response_text.strip("`").strip())

download_data(prompt)

def get_schemas(input):


# def load_data():
#     return