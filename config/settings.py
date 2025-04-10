import os

def get_default_data_path():
    return os.path.join(os.path.expanduser("~"), ".timemate", "data/sessions.json")

def get_default_settings_path():
    return os.path.join(os.path.expanduser("~"), ".timemate", "data/settings.json")