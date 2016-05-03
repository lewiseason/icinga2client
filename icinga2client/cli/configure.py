"""
Interactively configure the client.

::

  Usage:
    i2 configure
"""

from docopt import docopt
from ..config import Config
from ..helpers.interactive import prompt
from ..helpers.data import parse_docstring

doc = parse_docstring(__doc__)


def invoke(client, arguments, **kwargs):
    config = Config()

    print("The answers to the following questions will be stored (plaintext) "
          "in {} according to your umask.\n".format(config.config_path))

    print("Enter the icinga2 API url, without a trailing slash, or any part "
          "of the endpoint, such as `v1`.")
    config['url'] = prompt('URL', default=config.get('url', None))

    print("Enter the icinga2 ApiUser username")
    config['username'] = prompt('Username', default=config.get('username'))

    print("Enter the icinga2 ApiUser password")
    config['password'] = prompt('Password', hidden=True)
