# tele_web
import os, json
import telemancer.tele_tokens as tokens
import telemancer.tele_profiles as profiles

web_folder = "/web/"

def load_content(filename, web_context = ""):
    if filename == 'tokens.json':
        return get_tokens()
    if filename == 'profiles.json':
        return get_profiles()
    if filename == 'stats.json':
        return get_stats(web_context)
    
    try:
        with open(web_folder+filename, 'r') as file:
            print("Reading " + filename)
            contents = file.read()
            return contents
    except OSError as e:
        for file in os.listdir(web_folder):
            name = file.split('.')[0]
            if name == filename:
                return load_content(file)
        return ""

def process_api_call(endpoint, request):
    print("Processing API call for " + endpoint)
    
    post_body_start = request.find(b'\r\n\r\n') + 4
    post_body = request[post_body_start:]
    
    json_object = json.loads(post_body.decode())
    
    print("Body:")
    print(json_object)
    
    if endpoint == "deleteToken":
        tokens.remove_token(json_object['token_id'])
        return get_tokens()
    
    if endpoint == "addToken":
        tokens.add_token(json_object['token_name'], json_object['token_value'])
        return get_tokens()
        
    if endpoint == "updateProfiles":
        profiles.erase_profiles()
        for profile_num, name in json_object.items():
            profiles.add_profile(profile_num, name)
        return get_profiles()

    return ''
    
def get_tokens():
    return tokens.get_json_from_storage()

def get_profiles():
    return profiles.get_json_from_storage()

def get_stats(web_context):
    return json.dumps(web_context)