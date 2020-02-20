import inspect
import logging
from .splunk_event import SplunkEvent
from .utilities import get_class_from_frame, get_frame_from_log_record


class SplunkHandler(logging.Handler):
    def emit(self, record):
        logger_name = record.name
        if record.exc_info:
            event = self.event_from_exception_record(record)
        else:
            event = self.event_from_log_record(record)
        SplunkEvent().send_event(event, sourcetype=logger_name)

    @staticmethod
    def event_from_log_record(log_record):
        event_data = {
            "level": log_record.levelname,
        }
        if type(log_record.msg) is dict:
            event_data['message'] = log_record.msg
        else:
            event_data['message'] = log_record.getMessage()
        return event_data

    @staticmethod
    def event_from_exception_record(record):
        frame = get_frame_from_log_record(record)
        message = {
            'path': frame.f_code.co_filename,
            'line': frame.f_lineno,
            'method': frame.f_code.co_name,
            'class': get_class_from_frame(frame),
            'module': inspect.getmodule(frame).__name__,
            'message': record.getMessage(),
            'traceback': record.exc_text
        }
        event_data = {
            "level": record.levelname,
            "message": message
        }
        return event_data
