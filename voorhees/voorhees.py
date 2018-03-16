#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Modul to convert pythonic values into JSON values and in reverse
order."""

import re
from datetime import datetime, date
import uuid
import json

regex_date = re.compile("\d{4}-\d{2}-\d{2}")
regex_datetime = re.compile("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{6})?")

# Be Python3 and Python2 compatible
try:
    basestring
except NameError:
    basestring = str


def prettify(json_data):
    """Prettifies the json. Add indention and key sorting

    :json_data: JSON string
    :returns: Formatted JSON string

    """
    return to_json(from_json(json_data), indent=4, sort_keys=True)


def _json_deserial_hook(json_data):
    """JSON deserializer for objects not deserializable by default json
    code. Currently this is only `date` and `datetime`. Used in
    `from_json` as object hook.

    :json_data: Dictionary with serialized values.
    :returns: Dictionary with python values.
    """
    for k, v in json_data.items():
        if isinstance(v, basestring):
            if regex_datetime.match(v):
                try:
                    json_data[k] = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f")
                except:
                    json_data[k] = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%fZ")
            elif regex_date.match(v):
                json_data[k] = datetime.strptime(v, "%Y-%m-%d")
    return json_data


def from_json(json_data):
    """Will convert a given JSON string into a dictionary with python
    values.

    :json: JSON string.
    :returns: Dictionary with values.
    """
    return json.loads(json_data, object_hook=_json_deserial_hook)


def _json_serial_hook(obj):
    """JSON serializer for objects not serializable by default json
    code. Currently only `date` and `datetime` is supported

    :obj: Python value.
    :returns: Serialized value.
    """

    #if hasattr(obj, "__json__"):
    #    return obj.__json__()
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, (uuid.UUID)):
        return str(obj)
    raise TypeError("Type %s not serializable" % type(obj))


def serialize(obj):
    """Return a serialized dict from given object.
    :returns: dict
    """
    return json.loads(to_json(obj))


def to_json(obj, indent=None, sort_keys=False):
    """Will convert a given a dictionary with python values into a JSON
    string

    :json: Dictionary with values.
    :returns: JSON string.
    """
    return json.dumps(obj,
                      default=_json_serial_hook,
                      indent=indent,
                      sort_keys=sort_keys)
