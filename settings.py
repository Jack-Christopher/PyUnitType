import os
import sys
import json

def get_settings(src):
    settings_file = os.path.join(src, 'AFO.json')
    if not os.path.isfile(settings_file):
        print('[ERROR] AFO.json file not found in source folder.')
        sys.exit(1)
    with open(settings_file) as f:
        settings = json.load(f)
    return settings
