from flask import Flask, request, jsonify, render_template, redirect
import requests
import json
import os
import sqlite3 
import datetime

app = Flask(__name__)

dir = os.path.dirname(__file__)
db = os.path.join(dir, 'messages.db')

with sqlite3.connect(db) as connection:
    c = connection.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS hosts(id INTEGER PRIMARY KEY, url TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS people(id INTEGER PRIMARY KEY, name TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY, type TEXT, color TEXT, content TEXT, datetime TEXT, hosts_id INTEGER, people_id INTEGER, FOREIGN KEY(hosts_id) REFERENCES hosts(id), FOREIGN KEY(people_id) REFERENCES people(id))')

@app.route("/")
def index():
    with sqlite3.connect(db) as connection:
        c = connection.cursor()
        c.execute('SELECT * FROM messages')
        messages = c.fetchall()
        c.execute('SELECT * FROM hosts')
        hosts = c.fetchall()
        c.execute('SELECT * FROM people')
        people = c.fetchall()
    return render_template("index.html", messages=messages, hosts=hosts, people=people)

@app.route("/add_person", methods=["POST"])
def add_person():
    name = request.form["name"]
    with sqlite3.connect(db) as connection:
        c = connection.cursor()
        c.execute('INSERT INTO people(name) VALUES(?)', (name,))
    return redirect("/")

@app.route("/add_host", methods=["POST"])
def add_host():
    url = request.form["url"]
    with sqlite3.connect(db) as connection:
        c = connection.cursor()
        c.execute('INSERT INTO hosts(url) VALUES(?)', (url,))
    return redirect("/")

@app.route("/add_message", methods=["POST"])
def add_message():
    type = request.form["type"]
    color = request.form["color"]
    content = request.form["message"]
    current_datetime = datetime.datetime.now().replace(microsecond=0)
    current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    hosts_id = request.form["receiver"]
    people_id = request.form["sender"]
    with sqlite3.connect(db) as connection:
        c = connection.cursor()
        c.execute('INSERT INTO messages(type, color, content, datetime, hosts_id, people_id) VALUES(?, ?, ?, ?, ?, ?)', (type, color, content, current_datetime_str, int(hosts_id), int(people_id)))
    with sqlite3.connect(db) as connection:
        c = connection.cursor()
        c.execute('SELECT * FROM hosts WHERE id=?', (hosts_id,))
        host = c.fetchone() 
   
    print(hosts_id)
    print(host[1])
    # dictionary with data
    data = {
        "type": type,
        "color": color,
        "content": content,
    }
    # convert dictionary to JSON data
    json_data = json.dumps(data)
    # define HTTP headers for JSON data
    headers = {'Content-Type': 'application/json'}
    # try except block to handle error with host if not available
    try:
        # send POST request to host endpoint with JSON data and headers
        response = requests.post(host[1] + "/set_message", data=json_data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
        return jsonify({"status": "succes", "message": "The message was sent succesfully.", "response": response_data})
    except:
        return jsonify({"status": "error", "message": "An error occured while sending the message."})

if __name__ == "__main__":
    app.run()
