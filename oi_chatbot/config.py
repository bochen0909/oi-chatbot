import os
import yaml

OI_CHATBOT_HOME = os.getenv(
    'OI_CHATBOT_HOME', f'{os.getenv("HOME")}/.local/oi_chatbot')

if not os.path.exists(OI_CHATBOT_HOME):
    os.makedirs(OI_CHATBOT_HOME)


def load_config_file(filepath='config.yml'):
    with open(filepath, 'r') as f:
        config = yaml.safe_load(f)
    print(config)
    profiles = config.get('profiles', {})
    default_profile_name = config.get('default_profile', 'default')

    assert default_profile_name in profiles, f"Default profile '{default_profile_name}' not found in profiles"
    return profiles, profiles[default_profile_name], default_profile_name


profiles, default_profile, default_profile_name = load_config_file()

current_profile = default_profile
current_profile_name = default_profile_name
