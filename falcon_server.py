#! python
# -*- coding: utf-8 -*-
import falcon
import json
from datetime import datetime

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.


class TimeResource:

    def on_get(self, request, response):
        current_time_zone = 3

        try:
            timezone = int(request._params['timezone'])
            # print "time_zone params is %s" % type(timezone)
        except:
            timezone = current_time_zone

        """Handles GET requests"""
        response.status = falcon.HTTP_200  # This is the default status
        response.content_type = "application/json"
        response.set_header('Access-Control-Allow-Origin', '*')

        time_data = datetime.now()

        if timezone < current_time_zone:
            hour = time_data.hour - (current_time_zone - timezone)
        else:
            hour = time_data.hour + (timezone - current_time_zone)

        response.body = json.dumps({'hours': hour, 'minutes': time_data.minute})

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
time = TimeResource()

# things will handle all requests to the '/time' URL path
app.add_route('/time', time)