import requests
import configparser
import os
from requests.exceptions import HTTPError, RequestException
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from snowflake import connector

## read-in config
config = configparser.ConfigParser()
config.read("./config.ini")

## read-in input CSV


## get configs
api_key = config.get("OPENAI", "API_KEY")
endpoint = config.get("OPENAI", "ENDPOINT")
model = config.get("OPENAI", "MODEL")
tmp_dir = config.get("MOCKGEN", "TMP_DIR")
snowflake_private_key_path = config.get("SNOWFLAKE", "SNOWFLAKE_PRIVATE_KEY_PATH")

prompt = [{"role": "user", "content": "Give me three rows by three columns of mock CSV data, and do not give me any other text. Three tables. Table names are A, B, C, include separately inside CSV before the data."}]

def encode_private_key(private_key_content):

    private_key_en = private_key_content.encode()
    private_key_sr = serialization.load_pem_private_key(
        private_key_en, password=None, backend=default_backend()
    )
    private_key_bytes = private_key_sr.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return private_key_bytes

def get_schemas(input):

    with open(f"PRIVATE_KEY_PATH", "r") as f:
        private_key_contents = f.read()

    conn = connector.connect(
        user="devaccountairflow",
        account="bj69762.ca-central-1.aws",
        warehouse="ENGINEERS",
        database="DEVELOPMENT",
        schema="POINTS_PARTNER_FILE",
        private_key=encode_private_key(private_key_contents),
    )

    cursor = conn.cursor()
    
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


# def load_data():
#     return