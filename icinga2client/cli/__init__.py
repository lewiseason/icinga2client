"""
icinga2 command-line interface

Usage:
    i2 [--version] [--help] <command> [<arguments>...]

Commands:
    downtime
"""

from docopt import docopt, DocoptExit
import importlib

from icinga2client.api import ApiClient, Comment

doc = __doc__

def main():
    client = ApiClient('', verify=False)
    client.authenticate(username='', password='')

    arguments = docopt(doc, version="TODO", options_first=True)

    command = arguments['<command>']
    command_arguments = [command] + arguments['<arguments>']

    try:
        module = 'icinga2client.cli.{}'.format(command)
        invoke = importlib.import_module(module).invoke

        print invoke(client, command_arguments)

    except ImportError:
        # Warning: this is a little insidious, in that any ImportError
        # raised within the cli module will also be caught here.
        raise DocoptExit('Unknown command: ' + command)
