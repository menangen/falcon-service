#! python
# -*- coding: utf-8 -*-
import falcon
import json
import logs

from wsgiref import simple_server
from data_processing import TravelData

IP_ADDRESS_DEVELOPMENT_ONLY = '192.168.1.5'  # '127.0.0.1'


class FormResource:

    @staticmethod
    def on_post(request, response):

        # Enable logging
        log_request = logs.request
        log_response = logs.response

        if request.content_length in (None, 0):
            # Nothing to do
            return
        else:
            error_message = ""

        body = request.stream.read()
        # Error in body (sending ajax error / bad connection)
        if not body:
            error_message = "Empty request body!"
            log_request.warning("{0} from IP route {1}", error_message, request.access_route)

            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')
        else:
            # Normal body read
            log_request.debug("Incoming request from {0} body: {1}", request.access_route, body)

            try:
                request_data = json.loads(body.decode('utf-8'))
                log_request.debug("request_data: {0}", request_data)

                # Request data
                ip_address = request.access_route[0]
                # Form data:
                username = request_data.get("username", "")
                email = request_data.get("email", "")
                sex = request_data.get("sex", "")
                country = request_data.get("country", "")
                message = request_data.get("message", "")

                # Send data to processing engine (check non empty fields)
                travel_data = TravelData(
                    ip=ip_address,
                    username=username,
                    email=email,
                    sex=sex,
                    country=country,
                    message=message)

                log_request.debug("Valid Form data? : {0}", travel_data.is_valid())

                # Saving data to Database
                travel_data.save()

            except Exception as e:
                log_request.warning(e)
                # log_request.warning("Not valid JSON!")
                # error_message = "Error in json"
                error_message = e.__repr__()

            """Handles GET requests"""
            response.status = falcon.HTTP_200  # This is the default status
            response.content_type = "application/json"
            response.set_header('Access-Control-Allow-Origin', '*')

            if error_message:
                response_data = {"status": "error", "message": error_message}
            else:
                response_data = {"status":  "ok"}

            response.body = json.dumps(response_data)

            # Logging response
            log_response.debug(response_data)

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
ajaxForm = FormResource()

# things will handle all requests to the '/time' URL path
app.add_route('/travel', ajaxForm)

if __name__ == '__main__':
    print('Dev server started on {0}:8080'.format(IP_ADDRESS_DEVELOPMENT_ONLY))
    wsgi_server = simple_server.make_server(IP_ADDRESS_DEVELOPMENT_ONLY, 8080, app)
    wsgi_server.serve_forever()

else:
    from models import database, Traveler
    from peewee import DatabaseError

    try:
        database.connect()
        logs.data_transaction.debug("Open connection to database")

        try:
            database.create_table(Traveler)
            logs.data_transaction.debug("Ok, tables is created!")
        except DatabaseError as e:
            logs.data_transaction.warning(e)

        database.close()
    except Exception as e:
        logs.data_transaction.critical(e)