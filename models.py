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
                                       host='172.17.0.3')  # Postgresql port in Docker container
except:
    logs.data_transaction.critical("ORM Peewee instance error. Check installation")


class Traveler(Model):
    ip = CharField(max_length=45, index=True)
    username = CharField(max_length=64, index=True)
    email = CharField(max_length=64, index=True)
    sex = BooleanField(null=False)
    country = CharField(max_length=32)
    message = TextField()

    class Meta:
        database = database