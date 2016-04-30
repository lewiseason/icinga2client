import json
import requests as requests_lib
from multipledispatch import dispatch

from .helpers import dict_no_nones, to_timestamp

class RequestManager:
    api_prefix = 'v1'
    default_headers = {
        'Accept': 'application/json'
    }

    request_parameters = {}

    def __init__(self, base_uri):
        self.base_uri = base_uri

    def set_option(self, option, value):
        self.request_parameters[option] = value

    def url(self, command):
        return '{base}/{prefix}/{command}'.format(
            base=self.base_uri.rstrip('/'),
            prefix=self.api_prefix,
            command=command.lstrip('/'))

    def request(self, method, command, data=None, headers={}):
        """
        Make an API request.

        :param str method: The HTTP method/verb to use
        :param str command: The last part of the URI after the prefix, e.g.: ``objects/hosts``
        :param dict data: Data to be passed as the request body.
            Note: If ``data`` is supplied, and ``method`` is ``get``, the method will be
            rewritten, and the X-HTTP-Method-Override header will be set.
        :param dict headers: Any additional headers/overrides should be passed here
        :return: JSON-decoded response from the server
        :rtype: dict
        """

        method = method.lower()

        final_headers = self.default_headers.copy()
        final_headers.update(headers)

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

    def schedule_downtime(self, object_type, object_filter, start, end, comment, duration=False):
        return self.request('post', 'actions/schedule-downtime', {
            'type': object_type.title(),
            'filter': object_filter,
            'author': comment.author,
            'comment': comment.text,
            'start_time': to_timestamp(start),
            'end_time': to_timestamp(end),
            'duration': duration,
            'fixed': not bool(duration),
        })

    @dispatch(str, str)
    def remove_downtime(self, object_type, object_filter):
        return self.request('post', 'actions/remove-downtime', {
            'type': object_type.title(),
            'filter': object_filter,
        })

    @dispatch(list)
    def remove_downtime(self, downtimes):
        return self.request('post', 'actions/remove-downtime', {
            'downtime': downtimes,
        })

    @dispatch(str)
    def remove_downtime(self, downtime):
        return self.remove_downtime([downtime])

    def acknowledge_problem(self, object_type, object_filter, comment, expiry=None, sticky=True, notify=True):
        return self.request('post', 'actions/acknowledge-problem', dict_no_nones({
            'type': object_type.title(),
            'filter': object_filter,
            'author': comment.author,
            'comment': comment.text,
            'expiry': expiry,
            'sticky': sticky,
            'notify': notify,
        }))

    def remove_acknowledgement(self, object_type, object_filter):
        return self.request('post', 'actions/remove-acknowledgement', {
            'type': object_type.title(),
            'filter': object_filter,
        })

    def objects(self, object_type, filter=None, attrs=None, joins=None):
        """
        Retrieve a list of configuration objects from the server,
        with options to filter, limit attributes and side-load related objects.

        :param str object_type: The plural of the object type to be queried
        :param str filter: Filter the returned objects according to this string
        :param list attrs: Only return these attributes of each object
        :param list joins: Side-load objects or attributes
        """

        return self.request('get', 'objects/' + object_type.lower(), dict_no_nones({
            'filter': filter,
            'attrs': attrs,
            'joins': joins
        }))

    def status(self, component=None):
        """
        Fetch application status from the server.

        :param str component: If specified, limit status information to the specified component
        """

        command = 'status/' + component if component else 'status'
        return self.request('get', command)
