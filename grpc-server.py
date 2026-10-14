#!/usr/bin/env python3

import grpc
from concurrent import futures
import io
import base64
from PIL import Image

import lab6_pb2
import lab6_pb2_grpc


class Lab6Server(lab6_pb2_grpc.Lab6ServiceServicer):

    def add(self, request, context):
        a = request.a
        b = request.b
        result = a + b
        return lab6_pb2.addReply(sum=result)

    def dotproduct(self, request, context):
        
        a = request.a
        b = request.b

        if len(a) != len(b):
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Vectors must have equal lengths"
            )
        result = sum(x * y for x, y in zip(a, b))

        return lab6_pb2.dotProductReply(
            dotproduct=result
        )

    def rawimage(self, request, context):

        img = Image.open(io.BytesIO(request.img))

        return lab6_pb2.imageReply(
            width=img.size[0],
            height=img.size[1]
        )

    def jsonimage(self, request, context):

        image_bytes = base64.b64decode(request.img)

        img = Image.open(io.BytesIO(image_bytes))

        return lab6_pb2.imageReply(
            width=img.size[0],
            height=img.size[1]
        )


def serve():

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    lab6_pb2_grpc.add_Lab6ServiceServicer_to_server(
        Lab6Server(),
        server
    )

    server.add_insecure_port('[::]:50051')

    server.start()

    print("gRPC server running on port 50051")

    server.wait_for_termination()


if __name__ == '__main__':
    serve()