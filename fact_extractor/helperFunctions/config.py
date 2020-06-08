import os
from configparser import ConfigParser, NoOptionError, NoSectionError

from helperFunctions.file_system import get_src_dir


def default_config():
    return load_config('main.cfg')


def load_config(config_file_name):
    '''
    loads config of CONFIG_DIR/config_file_name
    Returns config object
    '''
    config = ConfigParser()
    config_path = '{}/{}'.format(get_config_dir(), config_file_name)
    if os.path.exists(config_path):
        config.read(config_path)
        return config
    raise RuntimeError('Cannot load config')


def get_config_dir():
    '''
    Returns the absolute path of the config directory
    '''
    return '{}/config'.format(get_src_dir())


def read_list_from_config(config_file: ConfigParser, section: str, key: str, default=None):
    if default is None:
        default = []

    if not config_file:
        return default

    try:
        config_entry = config_file.get(section, key)
    except (NoOptionError, NoSectionError):
        return default

    if not config_entry:
        return default
    return [item.strip() for item in config_entry.split(',') if item]
