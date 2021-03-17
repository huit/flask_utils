#!/usr/bin/env python3
"""
Module for interacting with the database
"""
# -*- encoding: utf-8 -*-

#============================================================================================
# Imports
#============================================================================================
# Standard imports

# Third-party imports
import cx_Oracle
from flask import make_response, jsonify

from pydb.oracle_db import OracleDB

# Local imports
from flask_utils.config_util import get_config_util
from flask_utils.logger_util import get_common_logger

from pylog.pylog import get_common_logging_format

logger = get_common_logger(__name__)


class DBUtil:
    """
    Class for interacting with the database
    """

    def __init__(self):
        self._oracle_db = OracleDB(oracle_config=get_config_util().db_config,
                                   logging_level=logger.level,
                                   logging_format=get_common_logging_format())

    def execute_query(self, query_string, args=None):
        """
        Function for executing a query against the database via the session pool
        """
        try:
            return self._oracle_db.execute_query(query_string, args)

        except Exception as err:
            obj, = err.args
            logger.error("Context: %s", obj.context)
            logger.error("Message: %s", obj.message)
            return make_response(jsonify(
                message=str("Unable to execute query against the database")
            ), 500)

    def execute_update(self, pool, query_string, args=None):
        """
        Function for executing an insert/update query against the database via the session pool
        """
        try:
            self._oracle_db.execute_update(query_string=query_string, args=args)

        except Exception as err:
            obj, = err.args
            logger.error("Context: %s", obj.context)
            logger.error("Message: %s", obj.message)
            raise Exception(err)
