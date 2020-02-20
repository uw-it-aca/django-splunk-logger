import requests
import socket
import json
from django.conf import settings


class SplunkEvent(object):
    def send_event(self, event, sourcetype="log"):
        url = "https://{}:{}/services/collector/event" \
            .format(settings.SPLUNK_ADDRESS,
                    settings.SPLUNK_EVENT_COLLECTOR_PORT)
        headers = {'Authorization': "Splunk {}".format(settings.SPLUNK_TOKEN)}
        host = socket.gethostname()
        event_data = {"sourcetype": sourcetype,
                      "event": event,
                      "host": host}
        requests.post(url,
                      headers=headers,
                      data=json.dumps(event_data),
                      verify=False)
