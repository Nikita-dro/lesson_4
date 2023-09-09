from peewee import *
from table_models import *
from flask import Flask, render_template

app = Flask(__name__)

Customers.create_table()
Tracks.create_table()

if not Customers.select():
    Customers.insert_many([('Dima', 'Charles'), ("Glenn", "Lee"), ("Mary", "Brown"), ('Dima', 'Charles')]).execute()
    Tracks.insert_many([("Bohemian", 354), ("Imagine", 184), ("Billie Jean", 294), ("Shape of You", 233)]).execute()


@app.get('/names/')
def names():
    list_names = [el.first_name for el in Customers.select(Customers.first_name).distinct()]
    return render_template("names.html", names=list_names)


if __name__ == "__main__":
    app.run()
