import argparse
import configparser
import logging

from common_helper_files import create_dir_for_file

from helperFunctions.config import get_config_dir, read_list_from_config
from version import __VERSION__


def setup_argparser(name, description, command_line_options, version=__VERSION__):
    parser = argparse.ArgumentParser(description='{} - {}'.format(name, description))
    parser.add_argument('-V', '--version', action='version', version='{} {}'.format(name, version))
    parser.add_argument('-o', '--output', dest='data_folder', help='Path to output directory', default=None)
    parser.add_argument('-l', '--log_file', help='Path to log file', default=None)
    parser.add_argument('-L', '--log_level', help='Define the log level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default=None)
    parser.add_argument('-d', '--debug', action='store_true', help='Print debug messages', default=False)
    parser.add_argument('-C', '--config_file', help='set path to config File', default='{}/main.cfg'.format(get_config_dir()))
    parser.add_argument('--exclude', metavar='GLOB_PATTERN', action='append', help='Exclude files paths that match %(metavar)s.', default=[])
    parser.add_argument('--blacklist', metavar='MIME_TYPE', action='append', help='Exclude files with %(metavar)s.', default=[])
    parser.add_argument('--disable-statistics', action='store_false', dest='statistics', help='Don\'t compute statistics or check for unpack data loss', default=None)
    parser.add_argument('FILE_PATH', type=str, help='Path to file that should be extracted')
    return parser.parse_args(command_line_options[1:])


def setup_logging(debug, log_file=None, log_level=None):
    log_level = log_level if log_level else logging.WARNING
    log_format = logging.Formatter(fmt='[%(asctime)s][%(module)s][%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)

    if log_file:
        create_dir_for_file(log_file)
        file_log = logging.FileHandler(log_file)
        file_log.setLevel(log_level)
        file_log.setFormatter(log_format)
        logger.addHandler(file_log)

    log_level = log_level if log_level else logging.INFO
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.DEBUG if debug else log_level)
    console_log.setFormatter(log_format)
    logger.addHandler(console_log)


def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def merge_options(arguments, config):
    # Merge exclude lists from config and CLI arguments
    exclude = read_list_from_config(config, 'unpack', 'exclude')
    config['unpack']['exclude'] = ", ".join(exclude + arguments.exclude)

    blacklist = read_list_from_config(config, 'unpack', 'blacklist')
    config['unpack']['blacklist'] = ", ".join(blacklist + arguments.blacklist)

    # Allow overriding options from CLI
    if arguments.data_folder:
        config['unpack']['data_folder'] = arguments.data_folder

    if arguments.statistics is not None:
        config['ExpertSettings']['statistics'] = str(arguments.statistics)

    return config
