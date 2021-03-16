#!/usr/bin/env python3

from pyconfig.pyconfig import Config, Stack, SecretService

from flask_utils.logger_util import get_common_logger

#============================================================================================
# Globals
#============================================================================================

logger = get_common_logger(__name__)

CONFIG_UTIL = None


class ConfigUtil:
    """
    All config values pulled from the OS environment
    """
    def __init__(self, stack: Stack = Stack.LOCAL,
                 secret_service: SecretService = SecretService.SECRETS_MANAGER,
                 ansible_vars_dir_path: str = "./ansible_vars"):
        """
        Retrieve values from OS environment
        :param stack: defaults to Stack.LOCAL
        :param secret_service: defaults to SecretService.SECRETS_MANAGER
        :param ansible_vars_dir_path: defaults to './ansible_vars'
        """
        self.config = Config(stack=stack, secret_service=secret_service, ansible_vars_dir_path=ansible_vars_dir_path)

        self._db_config = {
            "host": self.config.get_value("DB_HOST"),
            "port": self.config.get_value("DB_PORT"),
            "instance": self.config.get_value("DB_INSTANCE"),
            "user": self.config.get_value("DB_USER"),
            "pwd": self.config.get_value("DB_PWD")
        }

        self._api_config = {
            "api_key": self.config.get_value("ECS_APIKEY"),
            "title": self.config.get_value("APP_NAME"),
            "description": self.config.get_value("APP_DESCRIPTION")
        }

        # without either of these values, the app will fail
        if self._api_config['api_key'] is None:
            raise Exception('api_key is missing')
        if self._db_config['pwd'] is None:
            raise Exception('db password is missing')

        global CONFIG_UTIL
        CONFIG_UTIL = self

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


def get_config_util():
    """
    Function to retrieve the global application config
    """
    global CONFIG_UTIL
    if CONFIG_UTIL is None:
        CONFIG_UTIL = ConfigUtil()
    return CONFIG_UTIL
