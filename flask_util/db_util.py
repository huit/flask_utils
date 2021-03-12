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

# Local imports
from flask_util.config_util import get_config
from flask_util.logger_util import get_common_logger

logger = get_common_logger(__name__)


class DBUtil:
    """
    Class for interacting with the database
    """
    @staticmethod
    def get_session_pool(self):
        """
        Function for creating a session pool with the database
        """
        oracle_config = get_config().db_config

        if oracle_config.get('pool') is None:
            host = oracle_config.get('host')
            port = oracle_config.get('port')
            instance = oracle_config.get('instance')

            try:
                dsn_str = cx_Oracle.makedsn(host, port, service_name=instance)
                pool = cx_Oracle.SessionPool(
                    user=oracle_config.get('user'),
                    password=oracle_config.get('pwd'),
                    dsn=dsn_str,
                    min=2,
                    max=5,
                    increment=1,
                    threaded=True,
                    encoding="UTF-8"
                    )
            except cx_Oracle.DatabaseError as err:
                obj, = err.args
                logger.error("Context: %s", obj.context)
                logger.error("Message: %s", obj.message)
                return make_response(jsonify(
                    message=str("Error connecting to the database and creating a session pool")
                ), 500)
            oracle_config['pool'] = pool
            return pool
        else:
            return oracle_config['pool']

    @staticmethod
    def create_connection(pool):
        """
        Function for creating a connection with the database from a session pool
        """
        try:
            connection = pool.acquire()
        except cx_Oracle.DatabaseError as err:
            obj, = err.args
            logger.error("Context: %s", obj.context)
            logger.error("Message: %s", obj.message)
            return make_response(jsonify(
                message = str("Error acquiring database connection from the session pool")
            ), 500)
        return connection

    @staticmethod
    def make_dict(cursor):
        """
        Function for converting a query result row into a dictionary
        """
        column_names = [d[0] for d in cursor.description]
        def create_row(*args):
            return dict(zip(column_names, args))
        return create_row

    def execute_query(self, pool, query_string, args=None):
        """
        Function for executing a query against the database via the session pool
        """
        try:
            connection = self.create_connection(pool)
            cursor = connection.cursor()
            if args is not None:
                cursor.execute(query_string, args)
            else:
                cursor.execute(query_string)
            cursor.rowfactory = self.make_dict(cursor)
            query_result = cursor.fetchall()
            cursor.close()
            pool.release(connection)
        except cx_Oracle.DatabaseError as err:
            obj, = err.args
            logger.error("Context: %s", obj.context)
            logger.error("Message: %s", obj.message)
            return make_response(jsonify(
                message = str("Unable to execute query against the database")
            ), 500)
        return query_result
