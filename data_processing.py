#! python
# -*- coding: utf-8 -*-
import logs
from models import database, Traveler


class TravelData:

    def __init__(self, ip="0.0.0.0", username="Noname", email=None, sex=None, country=None, message=""):
        try:
            self.ip = ip
            self.username = unicode(username).strip()
            self.email = unicode(email).strip()
            self.sex = unicode(sex).strip().lower()
            self.country = unicode(country).strip()
            self.message = unicode(message).strip()
        except Exception as e:
            logs.data_validator.critical(e)

    def is_valid(self):

        # Should True flag and max counter for indicate completed data in ajax form <input>'s
        counter = 0
        form_fileds_number = 5

        # IP
        if 0 < len(self.ip) < 46:
            counter += 1
            logs.data_validator.debug("Valid IP address")
        else:
            logs.data_validator.warning("Not valid IP address")

        # Message
        if len(self.message) > 0:
            counter += 1
            logs.data_validator.debug("Valid message textInput")
        else:
            logs.data_validator.warning("Invalid (empty) message textInput")

        # Username
        if 0 < len(self.username) < 65:
            counter += 1
            logs.data_validator.debug("Valid username textInput")
        else:
            logs.data_validator.warning("Empty username textInput")
        # Email
        if 0 < len(self.email) < 65 and self.email.find("@") > 0:
            counter += 1
            logs.data_validator.debug("Valid email textInput")
        else:
            logs.data_validator.warning("Invalid email textInput")
        # Male / Female
        if self.sex in (u"male", u"female"):
            counter += 1
            logs.data_validator.debug("Valid male/female radio select")
        else:
            logs.data_validator.warning("Invalid male/female radio select")
        # Country
        if 0 < len(self.country) < 33:
            counter += 1
            logs.data_validator.debug("Valid country textInput")
        else:
            logs.data_validator.warning("Empty country textInput")

        return counter == 1 + form_fileds_number  # ip + form fields

    def save(self):
        if self.is_valid():
            # Connect to DB
            try:
                database.connect()
                logs.data_transaction.debug("Open connection to database")

                try:
                    # Populate data to Model
                    user = Traveler(
                        ip=self.ip,
                        username=self.username,
                        email=self.email,
                        sex=1 if self.sex == u"male" else 0,
                        country=self.country,
                        message=self.message
                    )
                    # Saving data in ORM
                    user.save()
                    logs.data_transaction.debug("Save data to PostgreSQL")

                except Exception as e:
                    logs.data_transaction.critical(e)
                    logs.data_transaction.critical("Can't save model in DB")

            except Exception as e:
                logs.data_transaction.critical(e)
                logs.data_transaction.critical("Database conection ERROR!")  # Do you create 'travel' database?"

                # Now create scheme
                try:
                    database.create_table(Traveler)
                    logs.data_transaction.debug("Ok, tables is created!")
                except Exception as e:
                    logs.data_transaction.critical(e)

        else:
            logs.data_transaction.warning("Can't save invalid form data into database")