from __future__ import print_function

import settings
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
    # open channel to tensorflow server
    channel = implementations.insecure_channel(
        settings.GAN_TF_SERVER_NAME,
        settings.GAN_TF_SERVER_PORT)
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

    # create predict request
    request = predict_pb2.PredictRequest()

    # Call GAN model to make prediction on the image
    request.model_spec.name = settings.GAN_MODEL_NAME
    request.model_spec.signature_name = settings.GAN_MODEL_SIGNATURE_NAME
    request.inputs[settings.GAN_MODEL_INPUTS_KEY].CopyFrom(
        tf.contrib.util.make_tensor_proto(image, shape=[1]))

    result = stub.Predict(request, 60.0)  # 60 secs timeout
    
    return result.outputs['scores']
