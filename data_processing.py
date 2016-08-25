#! python
# -*- coding: utf-8 -*-
import logs
from models import database, User


class TravelData:

    def __init__(self, username, email, sex, city, country, message, is_professional):
        try:
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
        message_flag = False

        if len(self.message) > 0:
            message_flag = True
            logs.data_validator.debug("Valid message textInput")
        else:
            logs.data_validator.warning("Invalid (empty) message textInput")

        if 0 < len(self.username) < 65:
            counter += 1
            logs.data_validator.debug("Valid username textInput")
        else:
            logs.data_validator.warning("Empty username textInput")

        if 0 < len(self.email) < 65 and self.email.find("@") > 0:
            counter += 1
            logs.data_validator.debug("Valid email textInput")
        else:
            logs.data_validator.warning("Invalid email textInput")

        if self.sex in (u"male", u"female"):
            counter += 1
            logs.data_validator.debug("Valid male/female radio select")
        else:
            logs.data_validator.warning("Invalid male/female radio select")

        if 0 < len(self.city) < 33:
            counter += 1
            logs.data_validator.debug("Valid city textInput")
        else:
            logs.data_validator.warning("Empty city textInput")

        if 0 < len(self.country) < 33:
            counter += 1
            logs.data_validator.debug("Valid country textInput")
        else:
            logs.data_validator.warning("Empty country textInput")

        if self.is_professional in (u"yes", u"no"):
            counter += 1
            logs.data_validator.debug("Valid isProfessionalTarget radio select")
        else:
            logs.data_validator.warning("Invalid isProfessionalTarget radio select")

        return message_flag and counter == 6

    def save(self):
        if self.is_valid():
            # Connect to DB
            try:
                database.connect()
                logs.data_transaction.debug("Open connection to database")

                logs.data_transaction.debug("Saving data to PostgreSQL")

                try:
                    # Populate data to Model
                    user = User(
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

                except Exception as e:
                    logs.data_transaction.critical(e)
                    logs.data_transaction.critical("Can't save user in DB")

            except Exception as e:
                logs.data_transaction.critical(e)
                logs.data_transaction.critical(
                    "Database conection ERROR!")  # Is created the project 'travel' database?"

        else:
            logs.data_transaction.warning("Can't save invalid form data into database")