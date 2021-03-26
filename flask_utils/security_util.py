#!/usr/bin/env python3

from functools import wraps
from flask import request, abort, jsonify, make_response
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from flask_utils.config_util import CONFIG_UTIL
from flask_utils.logger_util import get_common_logger

logger = get_common_logger(__name__)


#============================================================================================
# Decorators
#============================================================================================
def apikey_required(view_function):
    """
    Decorator for header API Key auth requirement for the API
    """
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        apikey = CONFIG_UTIL.api_config['api_key']
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == apikey:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


def api_endpoint_exception_handling(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as err:
            logger.error('Validation exception: %s', err, exc_info=True, stack_info=True)
            return make_response(jsonify(
                message=str(err.messages)
            ), 400)
        except HTTPException as err:
            return err.response
        except Exception as err:
            logger.error('Unhandled exception: %s', err, exc_info=True, stack_info=True)
            return make_response(jsonify(
                message=str(err)
            ), 500)

    return decorated_function
