import datetime
import json


def bytes2str(b: bytes) -> str:
    return b.decode() if b else None


def json_serialize_helper(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.datetime):
        serial = obj.strftime("%Y.%m.%d %H:%M:%S")
        return serial

    return obj.__dict__


def to_json(obj):
    return json.dumps(obj, indent=2, sort_keys=True, default=json_serialize_helper)
