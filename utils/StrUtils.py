import datetime


def json_serialize_helper(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.datetime):
        serial = obj.strftime("%Y.%m.%d %H:%M:%S")
        return serial

    return obj.__dict__
