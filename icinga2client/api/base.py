from . import filters as f
from .request_manager import RequestManager
from .authentication import AuthenticationManager
from .helpers import deep_merge


class ApiClient:
    global_request_parameters = {}

    def __init__(self, base_uri, verify=True):
        """
        :param str base_uri: URI of icinga2 api. Typically https://some-address:5665
        :param bool verify: Whether or not to verify TLS certificate trust
        """

        self.request_manager = RequestManager(base_uri)
        self.request_manager.set_option('verify', verify)

        self.authentication_manager = AuthenticationManager()

    def api_request(self, method, command, data=None, headers={}):
        return self.request_manager.request(method, command, data=data, headers=headers)

    def authenticate(self, **kwargs):
        options = self.authentication_manager.authenticate(**kwargs)

        for key, val in options.items():
            self.request_manager.set_option(key, val)

    def __getattr__(self, attr):
        if hasattr(self.request_manager, attr):
            return getattr(self.request_manager, attr)
        else:
            object.__getattribute__(self, attr)

    def schedule_host_downtime(self, hostname, start, end, comment, all_services=False, **kwargs):
        host = self.schedule_downtime('Host', f.host(hostname), start, end, comment, **kwargs)
        if all_services:
            services = self.schedule_downtime('Service', f.host(hostname), start, end, comment, **kwargs)
        else:
            services = {}

        return dict(deep_merge(host, services))

    def remove_host_downtime(self, hostname, all_services=False):
        host = self.remove_downtime('Host', f.host(hostname))
        if all_services:
            services = self.remove_downtime('Service', f.host(hostname))
        else:
            services = {}

        return dict(deep_merge(host, services))

    def schedule_service_downtime(self, hostname, service, start, end, comment, **kwargs):
        return self.schedule_downtime('Service', f.service(hostname, service), start, end, comment, **kwargs)

    def remove_service_downtime(self, hostname, service):
        return self.remove_downtime('Service', f.service(hostname, service))

    def schedule_hostgroup_downtime(self, group, start, end, comment, all_services=False, **kwargs):
        host = self.schedule_downtime('Host', f.hostgroup(group), start, end, comment, **kwargs)
        if all_services:
            services = self.schedule_downtime('Service', f.hostgroup(group), start, end, comment, **kwargs)

        return dict(deep_merge(host, services or []))

    def remove_hostgroup_downtime(self, group, all_services=False):
        host = self.remove_downtime('Host', f.hostgroup(group))
        if all_services:
            services = self.remove_downtime('Service', f.hostgroup(group))

        return dict(deep_merge(host, services or []))

    def schedule_servicegroup_downtime(self, group, start, end, comment, **kwargs):
        return self.schedule_downtime('Service', f.servicegroup(group), start, end, comment, **kwargs)

    def remove_servicegroup_downtime(self, group):
        return self.remove_downtime('Service', f.servicegroup(group))

    def acknowledge_host_problem(self, hostname, comment, **kwargs):
        return self.acknowledge_problem('Host', f.host(hostname), comment, **kwargs)

    def remove_host_acknowledgement(self, hostname):
        return self.remove_acknowledgement('Host', f.host(hostname))

    def acknowledge_service_problem(self, hostname, service, comment, **kwargs):
        return self.acknowledge_problem('Service', f.service(hostname, service), comment, **kwargs)

    def remove_service_acknowledgement(self, hostname, service):
        return self.remove_acknowledgement('Service', f.service(hostname, service))
