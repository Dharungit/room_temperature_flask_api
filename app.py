import os
from datetime import datetime, timezone
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()   # loads variables from .env to the environment

CREATE_ROOM_TABLE = "CREATE TABLE IF NOT EXISTS rooms (id SERIAL PRIMARY KEY, name TEXT);"

CREATE_TEMPS_TABLE = """CREATE TABLE IF NOT EXISTS temperatures (room_id INTEGER, temperature REAL, 
                        date TIMESTAMP, FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE);"""

INSET_INTO_ROOMS = "INSERT INTO rooms (name) values (%s) RETURNING id;"

INSERT_TEMP = (
    "INSERT INTO temperatures (room_id, temperature, date) VALUES (%s, %s, %s);"
)

GLOBAL_NUMBER_OF_DAYS = "SELECT COUNT(DISTINCT DATE(date)) AS days FROM temperatures;"

GLOBAL_AVG = "SELECT AVG(temperature) AS average FROM temperatures;"

ROOM_NAME = """SELECT name FROM rooms WHERE id = (%s)"""

ROOM_NUMBER_OF_DAYS = """SELECT COUNT(DISTINCT DATE(date)) AS days FROM temperatures WHERE room_id = (%s);"""

ROOM_ALL_TIME_AVG = (
    "SELECT AVG(temperature) as average FROM temperatures WHERE room_id = (%s);"
)

ROOM_TERM = ("""SELECT
    DATE(temperatures.date) as reading_date, AVG(temperatures.temperature)
FROM temperatures
WHERE temperatures.room_id = (%s)
GROUP BY reading_date
HAVING DATE(temperatures.date) > (SELECT MAX(DATE(temperatures.date))-(%s) FROM temperatures)""")

app = Flask(__name__)
url = os.environ.get("DATABASE_URL")    # gets variables from environment
connection = psycopg2.connect(url)  # connect to the database

@app.get("/")
def home():
    return "Server running..."


@app.post("/api/room")
def create_room():
    data = request.get_json()
    name = data["name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ROOM_TABLE)
            cursor.execute(INSET_INTO_ROOMS, (name,))
            room_id = cursor.fetchone()[0]
    return { "id": room_id, "message": f"Room {name} created."}, 201

@app.post("/api/temperature")
def add_temperature():
    data = request.get_json()
    room_id = data["room_id"]
    temperature = data["temperature"]
    try:
         date = datetime.strptime(data["date"], "%m-%d-%Y %H:%M:%S")
    except KeyError:
        date = datetime.now(timezone.utc)
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TEMPS_TABLE)
            cursor.execute(INSERT_TEMP, (room_id, temperature, date))
    
    return {"message": "Temperature added."}, 201


@app.get("/api/average")
def get_global_average():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GLOBAL_AVG)
            average = cursor.fetchone()[0]
            cursor.execute(GLOBAL_NUMBER_OF_DAYS)
            days = cursor.fetchone()[0]
    return {"average": round(average, 2), "days": days}, 200


@app.get("/api/room/<int:room_id>")
def get_room_all(room_id):

    args = request.args
    term = args.get("term")

    if term is not None:
        return get_room_term(room_id, term)
   
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(ROOM_NAME, (room_id,))
            name = cursor.fetchone()[0]
            cursor.execute(ROOM_ALL_TIME_AVG, (room_id,))
            average = cursor.fetchone()[0]
            cursor.execute(ROOM_NUMBER_OF_DAYS, (room_id,))
            days = cursor.fetchone()[0]
    return { "name": name, "average": round(average, 2), "days": days }


def get_room_term(room_id, term):
    terms = { "week": 7, "month": 30 }
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(ROOM_NAME, (room_id,))
            name = cursor.fetchone()[0]
            cursor.execute(ROOM_TERM, (room_id, terms[term]))
            dates_temperatures = cursor.fetchall()
    
    average = sum(day[1] for day in dates_temperatures) / len(dates_temperatures)

    return {
        "name": name,
        "temperatures": dates_temperatures,
        "average": round(average, 2)
    }
