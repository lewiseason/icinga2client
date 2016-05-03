"""
icinga2 command-line interface

::

  Usage:
    i2 [--version] [--help] [--porcelain] <command> [<arguments>...]

  Options:
    --porcelain -p      Produce machine-readable output

  Commands:
    configure           Interactively prompt for configuration options
    acknowledge         Acknowledge/unacknowledge host and service problems
    downtime            Schedule and remove downtime for various config objects
"""

from docopt import docopt, DocoptExit
import importlib

from ..api import ApiClient, Comment
from ..version import project, version
from ..config import Config
from ..helpers.data import parse_docstring

doc = parse_docstring(__doc__)

version_string = ' '.join([project, version])

COMMANDS = ['configure', 'downtime', 'acknowledge']
COMMANDS_NO_CONFIG = ['configure']


def main():
    arguments = docopt(doc, version=version_string, options_first=True)

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
