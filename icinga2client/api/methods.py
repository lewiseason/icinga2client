"""
.. _remove-downtime: http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/icinga2-api#icinga2-api-actions-remove-downtime
.. _schedule-downtime: http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/icinga2-api#icinga2-api-actions-schedule-downtime
.. _downtimes: http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/advanced-topics#downtimes
.. _filter: http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/icinga2-api#icinga2-api-filters
.. _parsedatetime: https://pypi.python.org/pypi/parsedatetime
"""  # nopep8

from ..helpers.data import to_timestamp, to_timedelta


class APIMethodsMixin:
    def schedule_downtime(self, object_type, object_filter, start, end,
                          comment, duration=False, trigger_name=None):
        """
        Schedule downtime for hosts and services.

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

        if duration:
            duration = to_timedelta(duration).seconds
        else:
            duration = False

        return self.request('post', 'actions/schedule-downtime', {
            'type': object_type.title(),
            'filter': object_filter,
            'author': comment.author,
            'comment': comment.text,
            'start_time': to_timestamp(start),
            'end_time': to_timestamp(end),
            'duration': duration,
            'fixed': not bool(duration),
            'trigger_name': trigger_name,
        })

    def remove_downtime(self, downtime):
        """
        Remove a named downtime. See also :py:meth:`remove_downtime_filter`.

        See `remove-downtime`_ documentation for further information.

        :param str downtime: The name of the downtime to remove.
        """
        return self.request('post', 'actions/remove-downtime', {
            'downtime': downtime
        })

    def remove_downtime_filter(self, object_type, object_filter):
        """
        Remove downtimes matching the specified filter.
        See also :py:meth:`remove_downtime`.

        :param str object_type: The object type to perform the action on.
            Either ``Host`` or ``Service``.
        :param str object_filter: A `filter`_ to apply.
        """

        return self.request('post', 'actions/remove-downtime', {
            'type': object_type.title(),
            'filter': object_filter,
        })
