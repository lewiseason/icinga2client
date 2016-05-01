import json
import requests as requests_lib

from . import filters as f
from .methods import APIMethodsMixin
from .authentication import AuthenticationManager
from ..helpers.data import deep_merge, dict_no_nones


class ApiClient(APIMethodsMixin):
    api_prefix = 'v1'
    default_headers = {
        'Accept': 'application/json'
    }
    request_parameters = {}

    def __init__(self, base_uri, verify=True):
        """
        :param str base_uri: URI of icinga2 api.
            Typically https://some-address:5665
        :param bool verify: Whether or not to verify TLS certificate trust
        """

        self.base_uri = base_uri
        self.set_request_option('verify', verify)

        self.authentication_manager = AuthenticationManager()

    def set_request_option(self, option, value):
        self.request_parameters[option] = value

    def url(self, command):
        return '{}/{}/{}'.format(self.base_uri.rstrip('/'), self.api_prefix,
                                 command.lstrip('/'))

    def request(self, method, command, data=None, headers={}, **kwargs):
        """
        Make an API request.

        :param str method: The HTTP verb used in the request.
        :param str command: The path of the command, excluding the prefix.
            For example: ``objects/hosts`` or ``actions/acknowledge-problem``.
        :param object data: Additional request data. Must be serializable by
            :func:`json.dumps`.
        :param dict headers: Any additional HTTP headers.
        """

        method = method.lower()

        if headers == {}:
            final_headers = self.default_headers
        else:
            final_headers = self.default_headers.copy()
            final_headers.update(headers)

        if not kwargs.get('preserve_none'):
            data = dict_no_nones(data)

        params = {}
        params.update(self.request_parameters)
        params['headers'] = final_headers
        params['data'] = json.dumps(data)

        # if method == 'get' and data:
        #     method = 'post'
        #     headers['X-HTTP-Method-Override'] = 'get'

        response = getattr(requests_lib, method)(self.url(command), **params)

        try:
            response.raise_for_status()

        except Exception as e:
            # TODO: err...
            print(response.content)
            raise e

        return response.json()

    def authenticate(self, **kwargs):
        options = self.authentication_manager.authenticate(**kwargs)

        for key, val in options.items():
            self.set_request_option(key, val)
