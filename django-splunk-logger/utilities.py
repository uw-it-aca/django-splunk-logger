
def get_frame_from_log_record(record):
    """
    Walks the traceback to find the inner most call that takes a request
    object, necessary for wrapped API calls
    """

    traceback = record.exc_info[2]
    traceback_with_req = traceback
    while traceback.tb_next:
        tb_next = traceback.tb_next
        if tb_next.tb_frame.f_locals.get('request', None):
            traceback_with_req = tb_next
        traceback = tb_next
    return traceback_with_req.tb_frame


def get_class_from_frame(frame):
    try:
        class_name = frame.f_locals['self'].__class__.__name__
    except KeyError:
        class_name = None
    return class_name
