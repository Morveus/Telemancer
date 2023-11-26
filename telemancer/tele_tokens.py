# tokens.py

import json
import utime
import hashlib
import binascii

filename = '/config/token_data.json'

def read_tokens():
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except:
        write_tokens([])
        return []

def get_json_from_storage():
    try:
        with open(filename, 'r') as file:
            return file.read()
    except:
        return ''

def write_tokens(tokens):
    with open(filename, 'w') as file:
        json.dump(tokens, file)

def generate_token_id(token_name, token_value):
    current_time = str(utime.time())
    data = token_name + token_value + current_time
    s = binascii.hexlify(hashlib.sha256(data.encode()).digest()).decode()

    return s

def add_token(token_name, token_value):
    tokens = read_tokens()
    
    # Check if token_name already exists
    for token in tokens:
        if token['token_name'] == token_name:
            # Token name already exists, handle as needed
            print(f"Token with name '{token_name}' already exists.")
            return  # Skip adding the new token

    # Token name does not exist, add the new token
    token_id = generate_token_id(token_name, token_value)
    tokens.append({"token_name": token_name, "token_value": token_value, "token_id": token_id})
    write_tokens(tokens)


def remove_token(token_id):
    tokens = read_tokens()
    tokens = [token for token in tokens if token['token_id'] != token_id]
    write_tokens(tokens)
    return read_tokens()
