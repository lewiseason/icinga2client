"""
::

  Usage:
    i2 acknowledge [remove] host <name> [options]
    i2 acknowledge [remove] service <hostname> <name> [options]

  Acknowledge Options:
    --expiry=<timespec>         Optional expiry time
    --sticky                    Acknowledge until full recovery
    --suppress-notifications    Do not generate any configured notifications
    --operator=<name>           Name of the operator scheduling the downtime
    --comment=<comment>         Comment describing the reason for the downtime
"""

from docopt import docopt
from ..helpers.data import FriendlyArguments, parse_docstring

from ..helpers.interactive import prompt_for_comment
from ..api import filters as f

doc = parse_docstring(__doc__)


def invoke(client, arguments, **kwargs):
    canonical = docopt(doc, argv=arguments, options_first=False)
    args = FriendlyArguments(canonical)

    if args.remove:
        response = unacknowledge(client, args)

    else:
        comment = prompt_for_comment(args.operator, args.comment)
        response = acknowledge(client, args, comment)

    print(response)


def unacknowledge(client, args):
    fn = client.remove_acknowledgement

    if args.host:
        return fn('Host', f.host(args.name))

    elif args.service:
        return fn('Service', f.service(args.hostname, args.name))


def acknowledge(client, args, comment):
    fn = client.acknowledge_problem
    notify = not bool(args['suppress-notifications'])

    common_args = {
        'comment': comment, 'expiry': args.expiry,
        'sticky': args.sticky, 'notify': notify
    }

    if args.host:
        return fn('Host', f.host(args.name), **common_args)

    elif args.service:
        return fn('Service', f.service(args.hostname, args.name),
                  **common_args)
