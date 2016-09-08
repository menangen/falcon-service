#! python
# -*- coding: utf-8 -*-
import logs
from models import database, Traveler

try:
    database.connect()
except Exception as e:
    logs.data_transaction.critical(e)


try:
    database.create_table(Traveler)
    print("Ok, tables is created!")
except Exception as e:
    logs.data_transaction.critical(e)
    print(e)