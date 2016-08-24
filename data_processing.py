#! python
# -*- coding: utf-8 -*-
import logs


class TravelData:

    def __init__(self, username, email, sex, city, country, message, is_professional):
        self.username = str(username).strip()
        self.email = str(email).strip()
        self.sex = str(sex).strip()
        self.city = str(city).strip()
        self.country = str(country).strip()
        self.message = str(message).strip()
        self.is_professional = str(is_professional).strip()

    def is_valid(self):

        # Should True flag and max counter for indicate completed data in ajax form <input>'s
        counter = 0
        message_flag = False

        if len(self.message) > 0:
            message_flag = True
            logs.data_validator.debug("Valid message textInput")
        else:
            logs.data_validator.warning("Invalid (empty) message textInput")

        if len(self.username) > 0:
            counter += 1
            logs.data_validator.debug("Valid username textInput")
        else:
            logs.data_validator.warning("Empty username textInput")

        if len(self.email) > 0 and self.email.find("@") > 0:
            counter += 1
            logs.data_validator.debug("Valid email textInput")
        else:
            logs.data_validator.warning("Invalid email textInput")

        if self.sex.lower() in ("male", "female"):
            counter += 1
            logs.data_validator.debug("Valid male/female radio select")
        else:
            logs.data_validator.warning("Invalid male/female radio select")

        if len(self.city) > 0:
            counter += 1
            logs.data_validator.debug("Valid city textInput")
        else:
            logs.data_validator.warning("Empty city textInput")

        if len(self.country) > 0:
            counter += 1
            logs.data_validator.debug("Valid country textInput")
        else:
            logs.data_validator.warning("Empty country textInput")

        if self.is_professional.lower() in ("yes", "no"):
            counter += 1
            logs.data_validator.debug("Valid isProfessionalTarget radio select")
        else:
            logs.data_validator.warning("Invalid isProfessionalTarget radio select")

        return message_flag and counter == 6

    def save(self):
        if self.is_valid():
            logs.data_transaction.debug("Saving data to PosgreSQL")
        else:
            logs.data_transaction.warning("Can't save invalid form data into database")