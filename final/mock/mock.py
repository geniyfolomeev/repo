import os
from flask import Flask, request, jsonify

app = Flask(__name__)

database = {}


@app.route('/vk_id/<username>', methods=['GET', 'DELETE'])
def get_user(username):
    if request.method == "GET":
        if username in database:
            return jsonify({"vk_id": database[username]}), 200
        return jsonify({}), 404
    elif request.method == "DELETE":
        if username in database:
            database.pop(username)
            return jsonify(f"User {username} deleted"), 200
        return jsonify(f"Not found"), 404


@app.route('/', methods=['GET', 'POST', 'PUT'])
def main():
    if request.method == "POST":
        for key in request.get_json():
            if key in database:
                return jsonify(f'User "{key}" already exists'), 409
            else:
                if request.get_json()[key] in database.values():
                    return jsonify(f'Choose another id'), 409
                database[key] = request.get_json()[key]
                return jsonify(f'User "{key}" successfully created'), 200
    elif request.method == "GET":
        return jsonify(database), 200
    elif request.method == "PUT":
        for key in request.get_json():
            if key in database:
                database[key] = request.get_json()[key]
                return jsonify(f'User "{key}" successfully updated'), 200
            else:
                database[key] = request.get_json()[key]
                return jsonify(f'User "{key}" created'), 201


if __name__ == "__main__":
    app.run(host=os.environ["MOCK_HOST"], port=int(os.environ["MOCK_PORT"]))
