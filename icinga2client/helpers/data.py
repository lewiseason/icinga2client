import parsedatetime
import datetime
import time

calendar = parsedatetime.Calendar()


def parse_docstring(doc):
    return doc.replace('::', '').strip()


def to_timestamp(string):
    return time.mktime(calendar.parse(string)[0])


def to_timedelta(string):
    now = datetime.datetime.now()
    then = calendar.parseDT(string, sourceTime=now)[0]
    return then - now


def dict_has_all(d, keys):
    return all(k in d for k in keys)


def dict_no_nones(d):
    return dict((k, v) for k, v in d.items() if v is not None)


def deep_merge(d1, d2):
    for k in set(d1.keys()).union(d2.keys()):
        if k in d1 and k in d2:
            if isinstance(d1[k], dict) and isinstance(d2[k], dict):
                yield (k, dict(deep_merge(d1[k], d2[k])))
            elif isinstance(d1[k], list) and isinstance(d2[k], list):
                yield (k, d1[k] + d2[k])
            else:
                # If the types don't match, we take the value from
                # the second dictionary
                yield (k, d2[k])
        elif k in d1:
            yield (k, d1[k])
        else:
            yield (k, d2[k])


class FriendlyArguments:
    def __init__(self, arguments):
        self.arguments = arguments

    def __getitem__(self, attr):
        return self.__getattr__(attr)

    def __getattr__(self, attr):
        for candidate in self._build_possible_attrs(attr):
            if candidate in self.arguments:
                return self.arguments.get(candidate)

        return object.__getattribute__(self, attr)

    def _build_possible_attrs(self, attr):
        return [
            attr,
            "<%s>" % attr,
            "--%s" % attr,
            "-%s" % attr
        ]
