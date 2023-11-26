# tele_web
import os
import telemancer.tele_tokens as tokens

web_folder = "/web/"

def load_content(filename):
    if filename == 'tokens.json':
        return get_tokens()
    
    try:
        with open(web_folder+filename, 'r') as file:
            print("Reading " + filename)
            contents = file.read()
            return contents
    except OSError as e:
        print("Error opening file:", e)
        print("Trying to find a file with the same name...")
        for file in os.listdir(web_folder):
            print(file)
            name = file.split('.')[0]
            
            print("Found: " + name + " -- " + filename + " -- " + file)
            if name == filename:
                return load_content(file)
        return ""

def get_tokens():
    tokens_list = str(tokens.read_tokens())
    return tokens_list