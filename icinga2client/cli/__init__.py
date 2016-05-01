"""
icinga2 command-line interface

Usage:
    i2 [--version] [--help] [--porcelain] <command> [<arguments>...]

Options:
    --porcelain -p      Produce machine-readable output

Commands:
    configure           Interactively prompt for configuration options
    downtime            Schedule and remove downtime for various config objects
"""

from docopt import docopt, DocoptExit
import importlib

from ..api import ApiClient, Comment
from ..config import Config

doc = __doc__

COMMANDS = ['configure', 'downtime']
COMMANDS_NO_CONFIG = ['configure']


def main():
    arguments = docopt(doc, version="TODO", options_first=True)

    command = arguments['<command>']
    command_arguments = [command] + arguments['<arguments>']

    config = Config()

    if command not in COMMANDS:
        raise DocoptExit('Unknown command: ' + command)

    if command not in COMMANDS_NO_CONFIG and len(config.keys()) == 0:
        raise DocoptExit('Not configured, try running: i2 configure')

    client = ApiClient(config.url, verify=False)  # TODO: Verify option
    client.authenticate(username=config.username, password=config.password)

    module = 'icinga2client.cli.{}'.format(command)
    invoke = importlib.import_module(module).invoke

    invoke(client, command_arguments, porcelain=arguments['--porcelain'])
