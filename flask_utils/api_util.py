#!/usr/bin/env python3

# -*- encoding: utf-8 -*-

#============================================================================================
# Imports
#============================================================================================
# Standard imports

# Third-party imports
from flask_restx import Api
from flask_utils.config_util import get_config

api_config = get_config().api_config

# Initialize a Flask-RestX API object

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Api-Key'
    }
}

api = Api(
    version='1.0',
    title=api_config.get('title'),
    description=api_config.get('description'),
    authorizations=authorizations,
    security='apikey'
    )
