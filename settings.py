import os
import sys
import json

def get_settings(src):
    settings_file = os.path.join(src, 'settings.json')
    if not os.path.isfile(settings_file):
        print('[ERROR] settings.json file not found in source folder.')
        sys.exit(1)
    with open(settings_file) as f:
        settings = json.load(f)
    return settings

def store_settings(src, data):
    settings_file = os.path.join(src, 'settings.json')
    with open(settings_file, 'w') as f:
        json.dump(data, f, indent=4)
    return settings_file
