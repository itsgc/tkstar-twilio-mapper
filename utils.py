import yaml

def make_settings(settingsfile_path):
    with open(settingsfile_path, 'r') as settingsfile:
        return yaml.load(settingsfile)
