"""
::

  Usage:
    i2 downtime [remove] host <name> [--all-services] [options]
    i2 downtime [remove] service <hostname> <name> [options]
    i2 downtime [remove] hostgroup <name> [--all-services] [options]
    i2 downtime [remove] servicegroup <name> [options]
    i2 downtime remove <name>

  Create Options:
    --all-services              Include all services when scheduling downtime
                                for hosts [default: false]
    --start=<timespec>          Start time [default: now]
    --end=<timespec>            End time [default: +2 hours]
    --duration=<timespec>       Duration (if flexible downtime)
    --operator=<name>           Name of the operator scheduling the downtime
    --comment=<comment>         Comment describing the reason for the downtime
    --trigger-name=<name>       Trigger (if triggered downtime)
"""

from docopt import docopt
from ..helpers.data import FriendlyArguments, deep_merge, parse_docstring

from ..helpers.interactive import prompt_for_comment
from ..api import filters as f

doc = parse_docstring(__doc__)


def invoke(client, arguments, **kwargs):
    canonical = docopt(doc, argv=arguments, options_first=False)
    args = FriendlyArguments(canonical)

    downtime_type = get_downtime_type(args)
    filter_fn = getattr(f, downtime_type) if downtime_type else None

    if args.remove:
        response = remove_downtime(client, args, filter_fn)

    else:
        comment = prompt_for_comment(args.operator, args.comment)
        response = schedule_downtime(client, args, filter_fn, comment)

        # TODO: This is hardly ideal
        for result in response['results']:
            print(result['name'])


def get_downtime_type(args):
    for candidate in ['host', 'service', 'hostgroup', 'servicegroup']:
        if getattr(args, candidate):
            return candidate


def remove_downtime(client, args, filter_fn):
    fn = client.remove_downtime_filter

    if args.host or args.hostgroup:
        response = fn('Host', filter_fn(args.name))
        if not args['all-services']:
            return response

        return dict(deep_merge(response, fn('Service', filter_fn(args.name))))

    elif args.servicegroup:
        return fn('Service', filter_fn(args.name))

    elif args.service:
        return fn('Service', filter_fn(args.hostname, args.name))

    else:
        return client.remove_downtime(args.name)


def schedule_downtime(client, args, filter_fn, comment):
    fn = client.schedule_downtime
    common_args = {
        'start': args.start, 'end': args.end, 'duration': args.duration,
        'comment': comment, 'trigger_name': args['trigger-name']
    }

    if args.host or args.hostgroup:
        response = fn('Host', filter_fn(args.name), **common_args)
        if not args['all-services']:
            return response

        return dict(deep_merge(response, fn('Service', filter_fn(args.name),
                               **common_args)))

    elif args.service:
        return fn('Service', filter_fn(args.hostname, args.name),
                  **common_args)

    elif args.servicegroup:
        return fn('Service', filter_fn(args.name), **common_args)
