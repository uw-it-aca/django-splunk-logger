from django.test import TestCase, override_settings
from unittest import mock
import logging
import json


@override_settings(
    LOGGING={
        'version': 1,
        'disable_existing_loggers': True,
        'handlers': {
            'splunk': {
                'class': 'django-splunk-logger.splunk_handler.SplunkHandler'
            }
        },
        'loggers': {
            'testlogger': {
                'handlers': ['splunk'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    },
    SPLUNK_ADDRESS='foobar',
    SPLUNK_EVENT_COLLECTOR_PORT='8088',
    SPLUNK_TOKEN='123asd'
)
class SplunkEvent(TestCase):
    @mock.patch('requests.post')
    def test_string_log(self, mock_post):
        logger = logging.getLogger("testlogger")
        logger.debug("test message")
        called_args, called_kwargs = mock_post.call_args

        mock_url = 'https://foobar:8088/services/collector/event'
        self.assertEqual(called_args[0], mock_url)

        mock_header = {'Authorization': "Splunk 123asd"}
        self.assertEqual(called_kwargs['headers'], mock_header)

        request_data = json.loads(called_kwargs['data'])
        self.assertEqual(request_data['sourcetype'], 'testlogger')
        self.assertEqual(request_data['event']['level'], 'DEBUG')
        self.assertEqual(request_data['event']['message'], 'test message')

    @mock.patch('requests.post')
    def test_dict_log(self, mock_post):
        logger = logging.getLogger("testlogger")
        log_dict = {'user': 'javerage', 'login_attempts': 42}
        logger.info(log_dict)

        called_args, called_kwargs = mock_post.call_args
        request_data = json.loads(called_kwargs['data'])
        self.assertEqual(request_data['event']['level'], 'INFO')
        self.assertDictEqual(request_data['event']['message'], log_dict)

    @mock.patch('requests.post')
    def test_exception_log(self, mock_post):
        logger = logging.getLogger("testlogger")
        try:
            1/0
        except ZeroDivisionError as ex:
            logger.exception(ex)

        called_args, called_kwargs = mock_post.call_args
        request_data = json.loads(called_kwargs['data'])

        self.assertEqual(request_data['event']['level'], 'ERROR')
        self.assertTrue("django-splunk-logger/test.py" in
                        request_data['event']['message']['path'])
        self.assertEqual(request_data['event']['message']['line'], 63)
        self.assertEqual(request_data['event']['message']['method'],
                         'test_exception_log')
        self.assertEqual(request_data['event']['message']['class'],
                         'SplunkEvent')
        self.assertEqual(request_data['event']['message']['module'],
                         'django-splunk-logger.test')
        self.assertEqual(request_data['event']['message']['message'],
                         'division by zero')
