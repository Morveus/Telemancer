# tele_web
import os, json
import telemancer.tele_tokens as tokens
import telemancer.tele_profiles as profiles
import telemancer.tele_buzzer as buzzer
from telemancer.tele_buttons import Button, ButtonConfig

web_folder = "/web/"

def load_content(filename, web_context = ""):
    if filename == 'tokens.json':
        return get_tokens()
    if filename == 'profiles.json':
        return get_profiles()
    if filename == 'stats.json':
        return get_stats(web_context)
    if filename == 'buttons.json':
        return get_buttons()
    
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
    
    if endpoint == "updateButton":
        button_config = ButtonConfig()
        button_config.update_button(json_object['profile'], json_object['name'],
                                    custom_name=json_object['custom_name'],
                                    repeatable=json_object['repeatable'],
                                    interval=json_object['interval'],
                                    url=json_object['url'],
                                    token_id=json_object['token_id'],
                                    payload=json_object['payload'])
        buzzer.play_startup_sound()
        return get_tokens()

    return ''
    
def get_tokens():
    return tokens.get_json_from_storage()

def get_buttons():
    button_config = ButtonConfig()
    buttons_list = button_config.load_buttons()
    buttons_dict_list = [button.to_dict() for button in buttons_list]
    json_data = json.dumps(buttons_dict_list)    
    return json_data

def get_profiles():
    return profiles.get_json_from_storage()

def get_stats(web_context):
    return json.dumps(web_context)