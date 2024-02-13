import yaml

def load_config():
    """Loads the config file"""
    with open('config/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

 