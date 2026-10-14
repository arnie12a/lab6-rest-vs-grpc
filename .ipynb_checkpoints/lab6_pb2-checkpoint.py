#!/usr/bin/env python3

import grpc
import argparse
import random
import base64
import time

import lab6_pb2
import lab6_pb2_grpc


def doAdd(stub, debug=False):

    request = lab6_pb2.addMsg(a=5, b=10)

    response = stub.add(request)

    assert response.sum == 15

    if debug:
        print(response)


def doDotProduct(stub, debug=False):

    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]

    request = lab6_pb2.dotProductMsg(a=a, b=b)

    response = stub.dotproduct(request)

    if debug:
        print(response)


def doRawImage(stub, debug=False):

    with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as f:
        img = f.read()

    request = lab6_pb2.rawImageMsg(img=img)

    response = stub.rawimage(request)

    assert response.width > 0
    assert response.height > 0

    if debug:
        print(response)


def doJsonImage(stub, debug=False):

    with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as f:
        img = f.read()

    encoded_img = base64.b64encode(img).decode('utf-8')

    request = lab6_pb2.jsonImageMsg(img=encoded_img)

    response = stub.jsonimage(request)

    assert response.width > 0
    assert response.height > 0

    if debug:
        print(response)


parser = argparse.ArgumentParser()

parser.add_argument('host')
parser.add_argument(
    'cmd',
    choices=['add', 'rawImage', 'dotProduct', 'jsonImage']
)
parser.add_argument('reps', type=int)
parser.add_argument('-p', '--port', type=int, default=50051)
parser.add_argument('-d', '--debug', action='store_true')

args = parser.parse_args()

if args.reps <= 0:
    parser.error("reps must be positive")

addr = f"{args.host}:{args.port}"

print(f"Running {args.reps} reps against {addr}")

with grpc.insecure_channel(addr) as channel:

    stub = lab6_pb2_grpc.Lab6ServiceStub(channel)

    operations = {
        'add': doAdd,
        'rawImage': doRawImage,
        'dotProduct': doDotProduct,
        'jsonImage': doJsonImage
    }

    operation = operations[args.cmd]

    start = time.perf_counter()

    for _ in range(args.reps):
        operation(stub, debug=args.debug)

    delta = ((time.perf_counter() - start) / args.reps) * 1000

    print("Took", delta, "ms per operation")