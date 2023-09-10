from table_models import *
from flask import Flask, render_template, request

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


def data_search(f_name=None, l_name=None) -> list:
    if f_name is not None:
        data = Customers.select().where(Customers.first_name == f_name.capitalize())
    else:
        data = Customers.select().where(Customers.last_name == l_name.capitalize())
    list_info = []
    for el in data:
        list_info.append(f'Id - {el.id}, first_name - {el.first_name}, last_name - {el.last_name}')
    return list_info


@app.get('/customers/')
def customer():
    id_customer = request.args.get('id', type=int)
    first_name = request.args.get('first_name', type=str)
    last_name = request.args.get('last_name', type=str)
    if id_customer or id_customer == 0:
        if 0 < id_customer <= Customers.select(fn.Max(Customers.id)).scalar():
            info = Customers.get(Customers.id == id_customer)
            return f'Id - {info.id}, first_name - {info.first_name}, last_name - {info.last_name}'
        else:
            return 'There is no such id or it is less than zero'
    elif first_name or last_name:
        if first_name:
            list_info = data_search(f_name=first_name)
        else:
            list_info = data_search(l_name=last_name)
        if list_info:
            return render_template("names.html", names=list_info)
        else:
            return "This name was not found in the database"
    else:
        list_all_customers = [(f'Id - {el.id}, first_name - {el.first_name}, '
                               f'last_name - {el.last_name}') for el in Customers.select()]
        return render_template("names.html", names=list_all_customers)


@app.get('/tracks/count')
def count_tracks():
    return f"The number of entries in the track table - {str(Tracks.select(fn.Max(Tracks.id)).scalar())}"


@app.get('/tracks/duration')
def tracks_duration():
    list_info = [' - '.join((el.name, f"{el.duration} seconds")) for el in Tracks.select()]
    return render_template("names.html", names=list_info)


if __name__ == "__main__":
    app.run()
