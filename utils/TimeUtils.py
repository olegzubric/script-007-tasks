import datetime


def floattime_to_datatime(t):
    # type: (float) -> datetime.datetime
    return datetime.datetime.utcfromtimestamp(t)
