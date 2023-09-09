from peewee import *


class Customers(Model):
    id = AutoField(primary_key=True)
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)

    class Meta:
        database = SqliteDatabase('Lesson_4.db')


class Tracks(Model):
    id = AutoField(primary_key=True)
    name = CharField()
    duration = FloatField()

    class Meta:
        database = SqliteDatabase('Lesson_4.db')