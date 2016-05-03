"""
.. _remove-downtime: http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/icinga2-api#icinga2-api-actions-remove-downtime
.. _schedule-downtime: http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/icinga2-api#icinga2-api-actions-schedule-downtime
.. _downtimes: http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/advanced-topics#downtimes
.. _acknowledge-problem: http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/icinga2-api#icinga2-api-actions-acknowledge-problem
.. _remove-acknowledgement: http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/icinga2-api#icinga2-api-actions-remove-acknowledgement
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

    def acknowledge_problem(self, object_type, object_filter, comment,
                            expiry=None, sticky=True, notify=True):
        """
        Acknowledge a host or service problem.

        See `acknowledge-problem`_ documentation for further information.

        :param str object_type: The object type to acknowledge.
            Either ``Host`` or ``Service``.
        :param str object_filter: A `filter`_ to apply when acknowledging
            the problem.
        :param Comment comment: Comment associated with the acknowledgement.
        :param str expiry: A timespec marking the expiry time of the
            notification, in a valid `parsedatetime`_ format.
        :param bool sticky: Whether the notification is sticky. If so, it will
            only be cleared when the host or service returns to a healthy
            state, otherwise the ack will be cleared on any state change.
        :param bool notify: Whether to generate any configured notifications
            associated with the host or service.
        """

        if expiry:
            expiry = to_timestamp(expiry)

        return self.request('post', 'actions/acknowledge-problem', {
            'type': object_type.title(),
            'filter': object_filter,
            'author': comment.author,
            'comment': comment.text,
            'expiry': expiry,
            'sticky': sticky,
            'notify': notify,
        })

    def remove_acknowledgement(self, object_type, object_filter):
        """
        Remove acknowledgements on a host or service.

        See `remove-acknowledgement`_ documentation for further information.

        :param str object_type: The object type to remove acknowledgements
            for. Either ``Host`` or ``Service``.
        :param str object_filter: A `filter`_ to apply when removing
            the problem acknowledgement.
        """
        return self.request('post', 'actions/remove-acknowledgement', {
            'type': object_type.title(),
            'filter': object_filter
        })
