#!/usr/bin/env python3

from functools import wraps
from flask import request, abort

from flask_utils.config_util import get_config_util


#============================================================================================
# Decorator
#============================================================================================
def apikey_required(view_function):
    """
    Decorator for header API Key auth requirement for the API
    """
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        apikey = get_config_util().api_config['api_key']
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == apikey:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function
