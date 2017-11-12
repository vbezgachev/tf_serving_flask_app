import logging.config

import settings
import utils
from flask import Flask, Blueprint
from flask_restplus import Resource, Api
from api.restplus import api
from api.gan.endpoints.client import ns as gan_client_namespace

# create Flask application
app = Flask(__name__)

# load logging confoguration and create log object
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def __get_flask_server_params__():
    '''
    Returns connection parameters of the Flask application

    :return: Tripple of server name, server port and debug settings
    '''
    server_name = utils.get_env_var_setting('FLASK_SERVER_NAME', settings.DEFAULT_FLASK_SERVER_NAME)
    server_port = utils.get_env_var_setting('FLASK_SERVER_PORT', settings.DEFAULT_FLASK_SERVER_PORT)

    flask_debug = utils.get_env_var_setting('FLASK_DEBUG', settings.DEFAULT_FLASK_DEBUG)
    flask_debug = True if flask_debug == '1' else False

    return server_name, server_port, flask_debug

def configure_app(flask_app, server_name, server_port):
    '''
    Configure Flask application

    :param flask_app: instance of Flask() class
    '''
    flask_app.config['SERVER_NAME'] = server_name + ':' + server_port
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

def initialize_app(flask_app, server_name, server_port):
    '''
    Initialize Flask application with Flask-RestPlus

    :param flask_app: instance of Flask() class
    '''
    blueprint = Blueprint('tf_api', __name__, url_prefix='/tf_api')

    configure_app(flask_app, server_name, server_port)
    api.init_app(blueprint)
    api.add_namespace(gan_client_namespace)

    flask_app.register_blueprint(blueprint)


def main():
    server_name, server_port, flask_debug = __get_flask_server_params__()
    initialize_app(app, server_name, server_port)
    log.info(
        '>>>>> Starting TF Serving client at http://{}/ >>>>>'.format(app.config['SERVER_NAME'])
        )
    app.run(debug=flask_debug, host=server_name)

if __name__ == '__main__':
    main()
