#!/usr/bin/env python3

import time
import logging

from flask import g, request, json

from pylog.pylog import get_common_logger_for_module


#============================================================================================
# Logging
#============================================================================================
def get_common_logger(module_name):
    """
    Function to create and return a new logger for a module
    """
    return get_common_logger_for_module(module_name=module_name, level=logging.INFO)


logger = get_common_logger(__name__)


def add_pre_post(app):
    @app.before_request
    def start_timer():
        """
        Preserve the starting time for a request
        """
        g.start = time.time()

    @app.before_request
    def log_request():
        """
        Preserve the starting time for a request
        """
        if request.path == '/favicon.ico':
            pass
        elif request.path.startswith('/static'):
            pass
        elif request.path.startswith('/swagger'):
            pass
        elif request.path == '/':
            pass
        else:
            ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)

            host = request.host.split(':', 1)[0]
            args = dict(request.args)

            g.consumer = request.headers.get('X-Consumer', default='UNKNOWN')

            log_message = json.loads('{"request": []}')
            log_message["request"].append(
                {
                    "consumer": g.consumer,
                    "method": request.method,
                    "path": request.path,
                    "ip": ip_addr,
                    "host": host,
                    "params": args
                })

            request_id = request.headers.get('X-Request-ID')
            if request_id:
                log_message["request"].append({"request_id": request_id})

            logger.info(json.dumps(log_message))

    @app.after_request
    def log_response(response):
        """
        Logging after the request is processed
        """
        if request.path == '/favicon.ico':
            return response
        elif request.path.startswith('/static'):
            return response
        elif request.path.startswith('/swagger'):
            return response
        elif request.path == '/':
            response.direct_passthrough = False
            return response
        else:
            now = time.time()
            duration = round(now - g.start, 2)
            ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)

            host = request.host.split(':', 1)[0]
            args = dict(request.args)

            log_message = json.loads('{"response": []}')
            log_message["response"].append(
                {
                    "consumer": g.consumer,
                    "method": request.method,
                    "path": request.path,
                    "status": response.status_code,
                    "duration": duration,
                    "ip": ip_addr,
                    "host": host,
                    "params": args
                })

            request_id = request.headers.get('X-Request-ID')
            if request_id:
                log_message["request"].append({"request_id": request_id})

            logger.info(json.dumps(log_message))

            return response
