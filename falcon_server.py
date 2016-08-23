#! python
# -*- coding: utf-8 -*-
import falcon
import json
import sys

from logbook import Logger, StreamHandler, FileHandler


class FormResource:

    @staticmethod
    def on_post(request, response):
        # Enable logging to File
        log_to_file = FileHandler('logs/service.log')
        log_to_file.push_application()

        # Enable logbook logger Stream to output
        #StreamHandler(sys.stdout).push_application()

        log_request = Logger('FormResource:request.stream.read')
        log_response = Logger('FormResource:response.body')

        if request.content_length in (None, 0):
            # Nothing to do
            return

        body = request.stream.read()
        # Error in body (sending ajax error / bad connection)
        if not body:
            log_request.warning("Empty request body!")
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')
        else:
            # Normal body read
            log_request.info(body)

            try:
                request_data = json.loads(body.decode('utf-8'))
                log_request.info(request_data)

                username = request_data.get("username", "")
                # print "time_zone params is %s" % type(timezone)
                log_request.info("Username is")
                log_request.info()

            except:
                log_request.warning("Not valid JSON!")
                username = ""

            """Handles GET requests"""
            response.status = falcon.HTTP_200  # This is the default status
            response.content_type = "application/json"
            response.set_header('Access-Control-Allow-Origin', '*')

            response_data = {"status":  "ok", "username": username}

            response.body = json.dumps(response_data)

            # Logging response
            log_response.info(response_data)

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
ajaxForm = FormResource()

# things will handle all requests to the '/time' URL path
app.add_route('/travel', ajaxForm)