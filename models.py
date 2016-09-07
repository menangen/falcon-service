#! python
# -*- coding: utf-8 -*-
import logs
from peewee import PostgresqlDatabase, Model, CharField, TextField, BooleanField

# Init DB
try:
    # PostgreSQL Config
    database = PostgresqlDatabase('travel',
                                       user='traveler',
                                       password='password',
                                       host='127.0.0.1')
except:
    logs.data_transaction.critical("ORM Peewee instance error. Check installation")


class Traveler(Model):
    ip = CharField(max_length=45, index=True)
    username = CharField(max_length=64, index=True)
    email = CharField(max_length=64, index=True)
    sex = BooleanField(null=False)
    city = CharField(max_length=32)
    country = CharField(max_length=32)
    message = TextField()
    is_professional = BooleanField(null=False)

    class Meta:
        database = database