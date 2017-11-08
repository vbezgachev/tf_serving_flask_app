import logging.config

import settings
from flask import Flask, Blueprint
from flask_restplus import Resource, Api
from api.restplus import api
from api.gan.endpoints.client import ns as gan_client_namespace

# create Flask application
app = Flask(__name__)

# load logging confoguration and create log object
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    '''
    Configure Flask application

    :param flask_app: instance of Flask() class
    '''
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

def initialize_app(flask_app):
    '''
    Initialize Flask application with Flask-RestPlus

    :param flask_app: instance of Flask() class
    '''
    configure_app(flask_app)
    api.init_app(app)
    api.add_namespace(gan_client_namespace)


def main():
    initialize_app(app)
    log.info(
        '>>>>> Starting TF Serving client at http://{}/ >>>>>'.format(app.config['SERVER_NAME'])
        )
    app.run(debug=settings.FLASK_DEBUG)

if __name__ == '__main__':
    main()
