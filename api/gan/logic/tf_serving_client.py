from __future__ import print_function

import tensorflow as tf

# Communication to TensorFlow server via gRPC
from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2


def make_prediction(image):
    '''
    Predict the house number on the image using GAN model

    :param image: images bytes
    '''
    # todo
    return 1
