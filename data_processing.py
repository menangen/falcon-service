#! python
# -*- coding: utf-8 -*-
import logs
from models import database, Traveler


class TravelData:

    def __init__(self, ip="0.0.0.0", username="Noname", email=None, sex=None, city=None, country=None, message="", is_professional=None):
        try:
            self.ip = ip
            self.username = unicode(username).strip()
            self.email = unicode(email).strip()
            self.sex = unicode(sex).strip().lower()
            self.city = unicode(city).strip()
            self.country = unicode(country).strip()
            self.message = unicode(message).strip()
            self.is_professional = unicode(is_professional).strip().lower()
        except Exception as e:
            logs.data_validator.critical(e)

    def is_valid(self):

        # Should True flag and max counter for indicate completed data in ajax form <input>'s
        counter = 0
        form_fileds_number = 7

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
        # City
        if 0 < len(self.city) < 33:
            counter += 1
            logs.data_validator.debug("Valid city textInput")
        else:
            logs.data_validator.warning("Empty city textInput")
        # Country
        if 0 < len(self.country) < 33:
            counter += 1
            logs.data_validator.debug("Valid country textInput")
        else:
            logs.data_validator.warning("Empty country textInput")
        # Target
        if self.is_professional in (u"yes", u"no"):
            counter += 1
            logs.data_validator.debug("Valid isProfessionalTarget radio select")
        else:
            logs.data_validator.warning("Invalid isProfessionalTarget radio select")

        return counter == 1 + form_fileds_number  # ip + form fileds

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
                        city=self.city,
                        country=self.country,
                        message=self.message,
                        is_professional=1 if self.is_professional == u"yes" else 0
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

        else:
            logs.data_transaction.warning("Can't save invalid form data into database")