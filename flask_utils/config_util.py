#!/usr/bin/env python3

import json

from pyconfig.pyconfig import Config, Stack, SecretService

from flask_utils.logger_util import get_common_logger

logger = get_common_logger(__name__)


class ConfigUtil:
    """
    All config values pulled from the OS environment
    """
    def __init__(self):
        self.config = None
        self._db_config = None
        self._api_config = None

    def setup(self, stack: Stack = Stack.LOCAL,
              secret_service: SecretService = SecretService.SECRETS_MANAGER,
              ansible_vars_dir_path: str = "./ansible_vars"):
        """
        Retrieve values from OS environment
        :param stack: defaults to Stack.LOCAL
        :param secret_service: defaults to SecretService.SECRETS_MANAGER
        :param ansible_vars_dir_path: defaults to './ansible_vars'
        """
        self.config = Config(stack=stack,
                             secret_service=secret_service,
                             ansible_vars_dir_path=ansible_vars_dir_path,
                             logging_level=logger.level)

        if self.get_value("DB_CONFIG"):  # db config is in json string
            self._db_config = json.loads(self.config.get_value("DB_CONFIG"))
        else:
            self._db_config = {
                "host": self.config.get_value("DB_HOST"),
                "port": self.config.get_value("DB_PORT"),
                "dbname": self.config.get_value("DB_SERVICE"),
                "username": self.config.get_value("DB_USER"),
                "password": self.config.get_value("DB_PWD")
            }

        # without db config the app will fail
        if not self.validate_db_config():
            raise Exception("Missing valid db config")

        self._api_config = {
            "api_key": self.config.get_value("APP_API_KEY"),
            "name": self.config.get_value("APP_NAME"),
            "description": self.config.get_value("APP_DESCRIPTION"),
            "url_prefix": self.config.get_value("APP_URL_PREFIX")
        }

        # without api_key, the app will fail
        if not self._api_config['api_key']:
            raise Exception('api_key is missing')

    @property
    def db_config(self):
        return self._db_config

    @property
    def api_config(self):
        return self._api_config

    def get_value(self, name):
        """
        :param name:
        :return:
        """
        return self.config.get_value(name)

    def validate_db_config(self):
        return self._db_config['host'] and \
               self.db_config['port'] and \
               self._db_config['dbname'] and \
               self._db_config['username'] and \
               self._db_config['password']


CONFIG_UTIL = ConfigUtil()