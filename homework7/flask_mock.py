import threading
from werkzeug.serving import make_server
from flask import Flask, jsonify, request
import settings

app = Flask(__name__)

USER_DATA = {}


@app.route('/user/<name>', methods=['GET', 'DELETE'])
def get_user(name):
    if request.method == "GET":
        if surname := USER_DATA.get(name):
            return jsonify(surname), 200
        else:
            return jsonify(f'No user found with name: "{name}"'), 404
    elif request.method == "DELETE":
        if name in USER_DATA:
            USER_DATA.pop(name)
            return jsonify(f"User {name} deleted"), 200
        else:
            return jsonify(f'No user found with name: "{name}"'), 404


@app.route('/user', methods=['POST', 'GET', 'PUT'])
def post_user():
    """Можно считать, что имя пользователя - primary key."""
    if request.method == "POST":
        for key in request.get_json():
            if key in USER_DATA:
                return jsonify(f'User "{key}" already exists'), 409
            else:
                USER_DATA[key] = request.get_json()[key]
                return jsonify(f'User "{key}" successfully created'), 200
    elif request.method == "GET":
        return jsonify(USER_DATA), 200
    elif request.method == "PUT":
        for key in request.get_json():
            if key in USER_DATA:
                USER_DATA[key] = request.get_json()[key]
                return jsonify(f'User "{key}" successfully updated'), 200
            else:
                USER_DATA[key] = request.get_json()[key]
                return jsonify(f'User "{key}" created'), 201


@app.route('/reset', methods=['GET'])
def reset():
    USER_DATA.clear()
    return jsonify(f'Database is clear now'), 200


def shutdown_mock():
    server.shutdown()
    thread.join()


@app.route('/shutdown', methods=["GET"])
def shutdown():
    shutdown_mock()
    return jsonify(f'Ok, exiting'), 200


def run_mock(host=settings.MOCK_HOST, port=int(settings.MOCK_PORT)):
    global server, thread
    server = make_server(host, port, app, True)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    return server
