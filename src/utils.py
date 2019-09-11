import json
from autohandshake import HandshakeSession

CONFIG_FILEPATH = '../config.json'

def load_config(config_filepath: str):
    """
    Load the configuration file
    :param config_filepath: the filepath to the config file
    :return: a dict of config values
    """
    with open(config_filepath, 'r') as file:
        return json.load(file)

CONFIG = load_config(CONFIG_FILEPATH)

class BrowsingSession(HandshakeSession):
    """
    A wrapper class around HandshakeSession that always logs into the same account.
    """

    def __init__(self, max_wait_time=300):
        super().__init__(CONFIG['handshake_url'], CONFIG['handshake_email'],
                         download_dir=CONFIG['download_dir'], max_wait_time=max_wait_time)
