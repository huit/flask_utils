#!/usr/bin/env python3

# -*- encoding: utf-8 -*-

#============================================================================================
# Imports
#============================================================================================
# Standard imports

# Third-party imports
from flask_restx import Api
from flask_utils.config_util import get_config

API = None


def get_api() -> Api:
    global API
    if API is None:
        setup_api()

    return API


def setup_api():
    """
    Initialize and return a Flask-RestX AP
    :return:
    """
    api_config = get_config().api_config

    authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-Api-Key'
        }
    }

    global API
    API = Api(
        version='1.0',
        title=api_config.get('title'),
        description=api_config.get('description'),
        authorizations=authorizations,
        security='apikey'
    )


def configure_app(flask_app):
    """
    Configure various Flask-RestX settings
    """
    flask_app.config['ERROR_404_HELP'] = False
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
    flask_app.config['RESTX_VALIDATE'] = True
    flask_app.config['RESTX_MASK_SWAGGER'] = False
    flask_app.config['ERROR_404_HELP'] = False
    flask_app.config['JSON_SORT_KEYS'] = False
