from getpass import getpass
from ..api import Comment


try:
    input = raw_input
except NameError:
    pass


def prompt(question, default=None, hidden=False):
    # TODO: Retry prompt if no default and no value
    if default:
        question += ' [%s]: ' % default
    else:
        question += ': '

    if hidden:
        default = None
        response = getpass(question)
    else:
        response = input(question)

    if response == '' and default:
        return default
    else:
        return response


def prompt_for_comment(username=None, comment=False):
    # TODO: Add handling to work out who the current user is.

    if not username:
        username = prompt('Operator Name')

    if not comment:
        comment = prompt('Comment')

    return Comment(username, comment)
