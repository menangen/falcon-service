#! python
# -*- coding: utf-8 -*-
import logs
from peewee import Model, CharField, PostgresqlDatabase

# Init DB
try:
    # PostgreSQL Config
    database = PostgresqlDatabase('travel',
                                       user='catadmin',
                                       password='1234',
                                       host='127.0.0.1')
except:
    logs.data_transaction.critical("ORM Peewee instance error. Check installation")


class User(Model):
    username = CharField(unique=True)

    class Meta:
        database = database