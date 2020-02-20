LOGGING = {
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
}