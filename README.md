[![Build Status](https://travis-ci.com/uw-it-aca/django-splunk-logger.svg?branch=master)](https://travis-ci.com/uw-it-aca/django-splunk-logger) [![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/django-splunk-logger/badge.svg?branch=master)](https://coveralls.io/github/uw-it-aca/django-splunk-logger?branch=master)
# django-splunk-logger
A Django/Python log handler for Splunk HTTP Event Collector

This supports logging exceptions, standard log strings, and dictionary data (sent as JSON).
Splunk sourcetype will be set to the logger name; hostname, log level, etc will all be set automatically 


## Setup Instructions

### Django Configuration
In your project's Django settings.py add the following 
configuration, modifying the your loggers to add the splunk handler
```python
INSTALLED_APPS += "django-splunk-logger"

LOGGING = {
    'handlers': {
        'splunk': {
            'class': 'django-splunk-logger.splunk_handler.SplunkHandler'
        }
    },
    'loggers': {
        'your_logger': {
            'handlers': ['splunk'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# HTTP Event Collector Token
SPLUNK_TOKEN = "your token"
# Splunk Server Address
SPLUNK_ADDRESS = "your splunk host"
# Event Collector Port (default: 8088)
SPLUNK_EVENT_COLLECTOR_PORT = "your splunk HEC port"
```

### Sample Event Payloads

#### String log

```json
{
	"sourcetype": "testlogger",
	"event": {
		"level": "DEBUG",
		"message": "test message"
	},
	"host": "ubuntu-dev-VirtualBox"
}
```

#### Dictionary log

```json
{
	"sourcetype": "testlogger",
	"event": {
		"level": "INFO",
		"message": {
			"user": "javerage",
			"login_attempts": 42
		}
	},
	"host": "ubuntu-dev-VirtualBox"
}
```

#### Exception log

```json
{
	"sourcetype": "testlogger",
	"event": {
		"level": "ERROR",
		"message": {
			"path": "/home/developer/django-splunk-logger/django-splunk-logger/test.py",
			"line": 63,
			"method": "test_exception_log",
			"class": "SplunkEvent",
			"module": "django-splunk-logger.test",
			"message": "division by zero",
			"traceback": "Traceback (most recent call last):\n  File \"/home/developer/splunk-handler/testapp/views.py\", line 15, in get\n    1/0\nZeroDivisionError: division by zero"
		}
	},
	"host": "ubuntu-dev-VirtualBox"
}
```
