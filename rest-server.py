#!/usr/bin/env python3

from flask import Flask, request, Response
import jsonpickle
from PIL import Image
import io
import argparse
import base64

# Initialize the Flask application
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)


@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
def add(a, b):
    response = {'sum': str(a + b)}
    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )


@app.route('/api/rawimage', methods=['POST'])
def rawimage():
    r = request

    # Convert the data to a PIL image type so we can extract dimensions
    try:
        ioBuffer = io.BytesIO(r.data)
        img = Image.open(ioBuffer)

        response = {
            'width': img.size[0],
            'height': img.size[1]
        }
    except:
        response = {'width': 0, 'height': 0}

    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )


@app.route('/api/dotproduct', methods=['POST'])
def dotproduct():

    # Extract JSON data from request
    data = request.get_json()

    # Extract vectors a and b
    a = data['a']
    b = data['b']

    # Make sure vectors have the same length
    if len(a) != len(b):
        return {'error': 'Vectors must have same length'}, 400

    # Calculate dot product
    result = sum(x * y for x, y in zip(a, b))

    # Prepare response
    response = {'dotproduct': result}

    response_pickled = jsonpickle.encode(response)

    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )
    

@app.route('/api/jsonimage', methods=['POST'])
def jsonimage():
    r = request

    # Convert the JSON image data to a PIL image type
    try:
        data = r.get_json()

        # Decode Base64 string into binary image data
        img_data = base64.b64decode(data['image'])

        ioBuffer = io.BytesIO(img_data)
        img = Image.open(ioBuffer)

        response = {
            'width': img.size[0],
            'height': img.size[1]
        }
    except Exception as e:
        print("Error processing JSON image:", e)
        response = {'width': 0, 'height': 0}

    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Flask REST server'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        default=5000,
        help='Port on which to run the server (default: 5000)'
    )

    args = parser.parse_args()

    # Start Flask app
    app.run(host='0.0.0.0', port=args.port)
