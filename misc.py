import datetime

def datetime_to_post_format(d, prefix=""):
    '''converts a datetime to dict, for certain CXDO POSTs'''
    assert isinstance(d, datetime.datetime)
    fields= ("minute", "hour", "day", "month", "year")
    return dict([ (prefix+f, getattr(d,f)) for f in fields])
