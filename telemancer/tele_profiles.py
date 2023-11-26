import json

filename = '/config/profile_data.json'

def read_profiles():
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except:
        write_profiles([])
        return []

def get_json_from_storage():
    try:
        with open(filename, 'r') as file:
            return file.read()
    except:
        return ''

def write_profiles(profiles):
    with open(filename, 'w') as file:
        json.dump(profiles, file)

def add_profile(profile_number, profile_name):
    profiles = read_profiles()
    
    # Check if profile_number already exists
    for profile in profiles:
        if profile['profile_number'] == profile_number:
            # Profile number already exists, handle as needed
            print(f"Profile with number '{profile_number}' already exists.")
            return  # Skip adding the new profile

    # Profile number does not exist, add the new profile
    profiles.append({"profile_number": profile_number, "profile_name": profile_name})
    write_profiles(profiles)

def remove_profile(profile_number):
    profiles = read_profiles()
    profiles = [profile for profile in profiles if profile['profile_number'] != profile_number]
    write_profiles(profiles)
    return read_profiles()

def erase_profiles():
    write_profiles([])

def init_profiles():
    profiles = read_profiles()
    if not profiles:
        default_profiles = [
            {"profile_number": 1, "profile_name": "Kodi Theater Room"},
            {"profile_number": 2, "profile_name": "Theater Sound System"},
            {"profile_number": 3, "profile_name": "Theater Lights"},
            {"profile_number": 4, "profile_name": "Theater Climate Control"}
        ]

        write_profiles(default_profiles)
