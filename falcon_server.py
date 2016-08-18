#! python
# -*- coding: utf-8 -*-
import falcon
import json

class FormResource:

    def on_post(self, request, response):


        try:
            username = request._params['username']
            # print "time_zone params is %s" % type(timezone)
        except:
            username = ""

        """Handles GET requests"""
        response.status = falcon.HTTP_200  # This is the default status
        response.content_type = "application/json"
        response.set_header('Access-Control-Allow-Origin', '*')

        response_data = {"status":  "ok", "username": username}

        response.body = json.dumps(response_data)

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
time = FormResource()

# things will handle all requests to the '/time' URL path
app.add_route('/travel', time)