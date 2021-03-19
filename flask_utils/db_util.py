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

from pydb.database import DatabaseType
from pydb.oracle_db import OracleDB
from pydb.sql_alchemy_oracle_db import SqlAlchemyOracleDB

# Local imports
from flask_utils.config_util import CONFIG_UTIL
from flask_utils.logger_util import get_common_logger

from pylog.pylog import get_common_logging_format

logger = get_common_logger(__name__)


class DBUtil:
    """
    Class for interacting with the database
    """

    def __init__(self):
        self._db = None

    def setup(self, db_type: DatabaseType = DatabaseType.ORACLE):
        db_config = CONFIG_UTIL.db_config
        if db_type == DatabaseType.ORACLE:
            self._db = OracleDB(host=db_config['host'],
                                port=db_config['port'],
                                service=db_config['service'],
                                user=db_config['user'],
                                pwd=db_config['pwd'],
                                logging_level=logger.level,
                                logging_format=get_common_logging_format())
        elif db_type == DatabaseType.SQL_ALCHEMY_ORACLE:
            self._db = SqlAlchemyOracleDB(host=db_config['host'],
                                          port=db_config['port'],
                                          service=db_config['service'],
                                          user=db_config['user'],
                                          pwd=db_config['pwd'],
                                          logging_level=logger.level,
                                          logging_format=get_common_logging_format())
        else:
            self._db = None

    def execute_query(self, query_string, args=None):
        """
        Function for executing a query against the database via the session pool
        """
        try:
            return self._db.execute_query(query_string, args)

        except Exception as err:
            obj, = err.args
            logger.error("Context: %s", obj.context)
            logger.error("Message: %s", obj.message)
            return make_response(jsonify(
                message=str("Unable to execute query against the database")
            ), 500)

    def execute_update(self, query_string, args=None):
        """
        Function for executing an insert/update query against the database via the session pool
        """
        try:
            self._db.execute_update(query_string=query_string, args=args)

        except Exception as err:
            obj, = err.args
            logger.error("Context: %s", obj.context)
            logger.error("Message: %s", obj.message)
            raise Exception(err)

    def health_check(self):
        """
        provides a means to verify connectivity with a simple query
        :return:
        """
        return self._db.health_check()

    def cleanup(self):
        if self._db is not None:
            self._db.cleanup()

    def create_connection(self):
        if self._db is not None:
            return self._db.create_connection()

    def get_session(self):
        if self._db is not None:
            return self._db.get_session()


DB_UTIL = DBUtil()
