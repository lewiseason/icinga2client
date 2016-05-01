def host(hostname):
    return 'host.name == "{}"'.format(hostname)


def service(hostname, service):
    return 'host.name == "{}" && service.name == "{}"'\
        .format(hostname, service)


def hostgroup(group):
    return '"{}" in host.group'.format(group)


def servicegroup(group):
    return '"{}" in service.group'.format(group)
