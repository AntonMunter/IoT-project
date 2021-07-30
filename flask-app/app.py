import time
import flask
import json
import mariadb
from flask import jsonify
from flask import request
import sys
from errorHandling import InvalidUsage
import db
from flask_cors import CORS, cross_origin
import os

app = flask.Flask(__name__)
cors = CORS(app)


# route to return all sensor data
@app.route('/api/data', methods=['GET'])
@cross_origin()
def data():
   param = request.args.get('size')

   if param is None:
      size = 1
   elif not len(param.strip()):
      raise InvalidUsage('Missing value', status_code=400)
   elif not param.strip().isnumeric():
      raise InvalidUsage('Value must be integer', status_code=400)
   else:
      size = int(param.strip())

   result = db.fetchData(size)

   return jsonify(result)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == "__main__":
   # socketio.run(app, host='0.0.0.0', port=5000, debug=True)
   app.run(host ='0.0.0.0', debug = True)