from flask import Flask, request, jsonify
from sense_hat import SenseHat
import sqlite3

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

sense = SenseHat()

r = (255, 0, 0)         # red
o = (255, 128, 0)       # orange
y = (255, 255, 0)       # yellow
g = (0, 255, 0)         # green
b = (0, 0, 255)         # blue
p = (255, 0, 255)       # purple
n = (255, 128, 128)     # pink
w = (255, 255, 255)     # white
k = (0, 0, 0)           # blank

# create POST endpoint to receive data and set LED matrix on sense hat to show message
@app.route('/set_message', methods=['POST'])
def set_message():
    if request.method == 'POST':
        type = request.json['type']
        color = request.json['color']
        content = request.json['content']

        if color == "blue":
            c = b
        elif color == "green":
            c = g
        elif color == "yellow":
            c = y
        elif color == "red":
            c = r
        elif color == "pink":
            c = n

        if type == "message":
            sense.show_message(content, 0.1, c)
            # return json response with OK status
            return jsonify({'status': 'Message set', 'type': type, 'color': color, 'message': content})
        elif type == "heart":
            sense.set_pixels([
                k, c, c, k, k, c, c, k,
                c, c, c, c, c, c, c, c,
                c, c, c, c, c, c, c, c,
                c, c, c, c, c, c, c, c,
                c, c, c, c, c, c, c, c,
                k, c, c, c, c, c, c, k,
                k, k, c, c, c, c, k, k,
                k, k, k, c, c, k, k, k
            ])
            # return json response with OK status
            return jsonify({'status': 'Heart set', 'type': type, 'color': color})
        elif type == "smiley":
            if content == "happy":
                sense.set_pixels([
                    k, k, k, k, k, k, k, k,
                    k, c, c, k, k, c, c, k,
                    k, c, c, k, k, c, c, k,
                    k, k, k, k, k, k, k, k,
                    c, c, k, k, k, k, c, c,
                    c, c, c, c, c, c, c, c,
                    k, c, c, c, c, c, c, k,
                    k, k, k, k, k, k, k, k])
                # return json response with OK status
                return jsonify({'status': 'Smiley set', 'type': type, 'color': color, 'mood': content})
            elif content == "sad":
                sense.set_pixels([
                    k, k, k, k, k, k, k, k,
                    k, c, c, k, k, c, c, k,
                    k, c, c, k, k, c, c, k,
                    k, k, k, k, k, k, k, k,
                    k, k, k, k, k, k, k, k,
                    k, c, c, c, c, c, c, k,
                    c, c, c, c, c, c, c, c,
                    c, c, k, k, k, k, c, c])
                # return json response with OK status
                return jsonify({'status': 'Smiley set', 'type': type, 'color': color, 'mood': content})
            else:
                sense.clear()
                return jsonify({'status': 'No smiley set', 'type': type, 'color': color, 'mood': 'Only happy or sad accepted as content'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
