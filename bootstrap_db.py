#! python
# -*- coding: utf-8 -*-
import logs
from models import database, User

try:
    database.connect()
except Exception as e:
    logs.data_transaction.critical(e)


try:
    database.create_table(User)
except Exception as e:
    logs.data_transaction.critical(e)

print("Ok, tables is created!")