import os
import json
from flask import Flask, request, render_template, current_app
from people import (get_people, add_people, edit_people,
                    delete_people)
from validation import get_data, get_data_filtered, add_data


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/api')
def api_base():
    response = {
        "base_url": request.base_url,
        "endpoints": [
            {
                "people": [
                    request.base_url + "/people",
                    request.base_url + "/people?offset=<offset>",
                    request.base_url + "/people/<id>",
                    {
                        "filter": [
                            request.base_url + "/people?name=<name>",
                            request.base_url + "/people?status=<status>",
                            request.base_url + "/people?gender=<gender>"
                        ]
                    }
                ],
                "systems":[
                    request.base_url + "/systems",
                ],
                "locations":[
                    request.base_url + "/locations",
                ]
            }
        ]
    }

    return current_app.response_class(
                json.dumps(
                    response,
                    indent=4,
                    sort_keys=False
                    ), mimetype="application/json")


methods = ['GET', 'POST', 'PUT', 'DELETE']
@app.route('/api/people', methods=methods)
@app.route('/api/people/<id>', methods=['GET'])
def api_people(id=None):

    if request.method == "POST":
        data = request.get_json()
        return add_data("people", data)

    elif request.method == "PUT":
        data = request.get_json()
        return edit_people(data)

    elif request.method == "DELETE":
        data = request.get_json()
        return delete_people(data)
    else:
        requests = len(request.args)

        if requests > 0:
            return get_data_filtered("people", request.args)
        else:
            return get_data("people", id)


@app.route('/api/systems', methods=methods)
@app.route('/api/systems/<id>', methods=['GET'])
def api_systems(id=None):
    if request.method == "POST":
        data = request.get_json()
        return add_system(data)

    elif request.method == "PUT":
        data = request.get_json()
        return edit_system(data)

    elif request.method == "DELETE":
        data = request.get_json()
        return delete_system(data)
    else:
        requests = len(request.args)

        if requests > 0:
            return get_data_filtered("systems", request.args)
        else:
            return get_data("systems", id)


@app.route('/api/locations', methods=methods)
@app.route('/api/locations/<id>', methods=['GET'])
def api_locations(id=None):
    if request.method == "POST":
        data = request.get_json()
        return add_system(data)

    elif request.method == "PUT":
        data = request.get_json()
        return edit_system(data)

    elif request.method == "DELETE":
        data = request.get_json()
        return delete_system(data)
    else:
        requests = len(request.args)

        if requests > 0:
            return get_data_filtered("locations", request.args)
        else:
            return get_data("locations", id)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
