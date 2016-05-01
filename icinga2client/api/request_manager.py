"""
.. _remove-downtime: http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/icinga2-api#icinga2-api-actions-remove-downtime
.. _schedule-downtime: http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/icinga2-api#icinga2-api-actions-schedule-downtime
.. _downtimes: http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/advanced-topics#downtimes
.. _filter: http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/icinga2-api#icinga2-api-filters
.. _parsedatetime: https://pypi.python.org/pypi/parsedatetime

"""

import json
import requests as requests_lib
from multipledispatch import dispatch

from ..helpers.data import dict_no_nones, to_timestamp

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
        """
        Schedule a downtime for hosts and services.

        See `schedule-downtime`_ documentation for further information, and
        `downtimes`_ for information about fixed and flexible downtimes.

        :param str object_type: The object type to perform the action on.
            Either ``Host`` or ``Service``.
        :param str object_filter: A `filter`_ to apply when scheduling
            the downtime.
        :param str start: A timespec marking the beginning of the downtime,
            in a valid `parsedatetime`_ format.
        :param str end: A timespec marking the end of the downtime,
            in a valid `parsedatetime`_ format.
        :param Comment comment: Comment object associated with the downtime.
        :param str duration: A timespec indicating the maximum duration of the
            downtime. This implies a ``flexible`` downtime.
        :param str trigger_name: Sets the trigger for a triggered downtime.
        """
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
        """
        Remove a named downtime. See also :py:meth:`remove_downtime_filter`.

        See `remove-downtime`_ documentation for further information.

        :param str downtime: The name of the downtime to remove.
        return self.request('post', 'actions/remove-downtime', {
            'type': object_type.title(),
            'filter': object_filter,
        })

    @dispatch(list)
    def remove_downtime(self, downtimes):
        """
        Remove downtimes matching the specified filter.
        See also :py:meth:`remove_downtime`.

        :param str object_type: The object type to perform the action on.
            Either ``Host`` or ``Service``.
        :param str object_filter: A `filter`_ to apply.
        """

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

        return self.request('get', 'objects/' + object_type.lower(), dict_no_nones({
            'filter': filter,
            'attrs': attrs,
            'joins': joins
        }))

    def status(self, component=None):
        command = 'status/' + component if component else 'status'
        return self.request('get', command)
