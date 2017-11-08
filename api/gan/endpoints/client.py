import logging
import io

from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.gan.logic.tf_serving_client import make_prediction
from werkzeug.datastructures import FileStorage

log = logging.getLogger(__name__)

# create dedicated namespace for GAN client
ns = api.namespace('gan_client', description='Operations for GAN client')

# Flask-RestPlus specific parser for image uploading
UPLOAD_KEY = 'image'
UPLOAD_LOCATION = 'files'
upload_parser = api.parser()
upload_parser.add_argument(UPLOAD_KEY,
                           location=UPLOAD_LOCATION,
                           type=FileStorage,
                           required=True)


@ns.route('/prediction')
class GanPrediction(Resource):
    @ns.doc('Predict the house number on the image using GAN model', responses={
        200: "Success",
        400: "Unexpected error"
    })
    @ns.expect(upload_parser)
    def post(self):
        image_file = request.files[UPLOAD_KEY]
        image = io.BytesIO(image_file.read())
        result = make_prediction(image)
        log.info('Prediction on the image gave %d', result)
        return {'prediction_result': result}, 200
