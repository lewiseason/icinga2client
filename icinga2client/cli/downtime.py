"""
Usage:
    i2 downtime [remove] host <hostname> [options] [--all-services]
    i2 downtime [remove] service <hostname> <service> [options]
    i2 downtime [remove] hostgroup <group> [options] [--all-services]
    i2 downtime [remove] servicegroup <group> [options]

Options:
    --start=<timespec>          Start time [default: now]
    --end=<timespec>            End time [default: +2hours]
    --duration=<duration>       Duration
"""

from docopt import docopt
from ..helpers.data import FriendlyArguments
from ..helpers.interactive import prompt_for_comment

doc = __doc__

# TODO
from ..api import Comment

def invoke(client, arguments):
    canonical = docopt(doc, argv=arguments, options_first=False)
    args = FriendlyArguments(canonical)

    if not args.remove:
        c = prompt_for_comment()

    if args.host:
        if args.remove:
            client.remove_host_downtime(args.hostname)
        else:
            client.schedule_host_downtime(args.hostname, args.start, args.end, c)

    elif arguments['service']:
        if arguments['remove']:
            client.remove_service_downtime()
        else:
            client.schedule_service_downtime()
    # elif arguments['hostgroup']:
    #     client.remove_hostgroup_downtime()
    # elif arguments['servicegroup']:
    #     client.remove_servicegroup_downtime()
    # else:
    #     # schedule-downtime
