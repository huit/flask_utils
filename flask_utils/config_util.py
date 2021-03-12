#!/usr/bin/env python

import yaml
import os
import boto3
import base64

from enum import Enum

from botocore.exceptions import ClientError

from flask_utils.logger_util import get_common_logger

# Set a minimum log level DEBUG, INFO, WARNING, ERROR

#============================================================================================
# Globals
#============================================================================================
CONFIG = None
NO_VALUE_FOUND = "NO VALUE FOUND"

logger = get_common_logger(__name__)


class Stack(Enum):
    LOCAL = "local"
    SAND = "sand"
    DEV = "dev"
    TEST = "test"
    STAGE = "stage"
    PROD = "prod"


class SecretService(Enum):
    SSM = "ssm"
    SECRETS_MANAGER = "secretsmanager"


class Config:
    """
    All config values pulled from the OS environment
    For local deployment, will populate OS environ with variables/values pulled from dev_ansible_vars.yml,
    adding secrets pulled from parameter store or secretsmanager, depending on self.SecretService
    For other environments, variables and values are pumped into the OS environ by the AWS task definition
    """

    APP_ENV_KEY = 'target_app_env'
    SECRETS_REF_KEY = 'target_app_secrets_ref'

    def __init__(self, stack: Stack = Stack.LOCAL,
                 secret_service: SecretService = SecretService.SECRETS_MANAGER,
                 ansible_var_dir_path: str = "/ansible_vars"):
        """
        Retrieve values from OS environment or read from config files
        :param stack: defaults to Stack.LOCAL
        :param ansible_var_dir_path: defaults to '/ansible_vars'
        """
        self.stack = stack
        self.config_stack = stack
        self.ansible_var_dir_path = ansible_var_dir_path
        self.secret_service = secret_service
        if self.stack == Stack.LOCAL:
            self.config_stack = Stack.DEV
            self.populate_os_env()

        self._db_config = {
            "host": self.get_value("DB_HOST"),
            "port": self.get_value("DB_PORT"),
            "instance": self.get_value("DB_INSTANCE"),
            "user": self.get_value("DB_USER"),
            "pwd": self.get_value("DB_PWD")
        }

        self._api_config = {
            "api_key": self.get_value("ECS_APIKEY"),
            "title": self.get_value("APP_NAME"),
            "description": self.get_value("APP_DESCRIPTION")
        }

        # without either of these values, the app will fail
        if self._api_config['api_key'] is None:
            raise Exception('api_key is missing')
        if self._db_config['pwd'] is None:
            raise Exception('db password is missing')

        global CONFIG
        CONFIG = self

    @property
    def db_config(self):
        return self._db_config

    @property
    def api_config(self):
        return self._api_config

    @staticmethod
    def get_value(name):
        """
        check in the OS ENV which is populated at command line
        :param name:
        :return:
        """
        return os.environ.get(name, NO_VALUE_FOUND)

    def populate_os_env(self):
        app_dict = self.populate_app_dict()
        self.populate_secrets(app_dict)
        self.populate_vars(app_dict)

    def populate_app_dict(self):
        yaml_file_name = f"{self.ansible_var_dir_path}/dev_ansible_vars.yml"
        with open(yaml_file_name) as yaml_file_obj:
            app_dict = yaml.load(yaml_file_obj, Loader=yaml.FullLoader)
        return app_dict

    def populate_secrets(self, app_dict):
        """
        Reads key/value pairs from dict
        target_app_secrets_ref:
          - ORDS_PWD: aais-oakdev-password
            ORACLE_PWD: aais-oakdev-password
            OTHER_KEY: adex-other-secret

        var_dict example:
            {'ORDS_PWD': 'aais-oakdev-password', 'ORACLE_PWD': 'aais-oakdev-password', 'OTHER_KEY: 'adex-other-secret'}
        this will populate the OS environ with variables names for the keys, with values looked up from the selected SecretService
        :param app_dict:
        :return:
        """
        logger.debug(f"=======INSIDE populate secrets =======")
        try:
            var_dict = app_dict.get(self.SECRETS_REF_KEY)[0]
            logger.debug(var_dict)
            for k, v in var_dict.items():
                os.environ[k] = f"{self.get_secret_value(v)}"
        except yaml.YAMLError as exc:
            logger.exception(exc)

    def populate_vars(self, app_dict):
        """
        parsing object list of key/value objects into dictionary
        for example:
        target_app_env:
          - name: ORACLE_HOST
            value: oakdev-rds-db.dev.ats.cloud.huit.harvard.edu
          - name: HTTPS_PORT
            value: 9024
          - name: ORACLE_PORT
            value: 8003
        output sample : {'ORACLE_HOST': 'oakdev-rds-db.dev.ats.cloud.huit.harvard.edu', 'HTTPS_PORT': 9024, 'ORACLE_PORT': 8003}

        :param app_dict:
        :return:
        """
        logger.debug(f"======= parsing config vars and values =======")
        try:
            var_dict = {}
            for item in app_dict.get(self.APP_ENV_KEY):
                for key, value in item.items():
                    if key == "name":
                        var_name = value
                    if key == "value":
                        var_value = value
                os.environ[var_name] = f"{var_value}"
            logger.debug(var_dict)
            return var_dict
        except yaml.YAMLError as exc:
            logger.exception(exc)

    @staticmethod
    def get_secret(name):
        secret_name = name
        session = boto3.session.Session()
        region_name = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        client = session.client(service_name="secretsmanager", region_name=region_name)
        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            if "SecretString" in get_secret_value_response:
                secret = get_secret_value_response["SecretString"]
            else:
                secret = base64.b64decode(get_secret_value_response["SecretBinary"])
        except ClientError as error:
            logger.error("Lookup " + secret_name + ": " + str(error))
            secret = error
        return secret

    @staticmethod
    def get_ssm_param(name):
        """
         Retrieve a parameter from SSM
         """
        session = boto3.session.Session()
        region_name = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        ssm_client = session.client(service_name="ssm", region_name=region_name)
        parameter = ssm_client.get_parameter(
            Name=name,
            WithDecryption=True)
        return parameter['Parameter']['Value']

    def get_secret_value(self, name):
        """
        get the value from env if not in the env get the value from secret manager and add it to the dictionary
        :param name:
        :return:
        """
        if self.secret_service == SecretService.SECRETS_MANAGER:
            l_secret = os.environ.get(name, self.get_secret(self.config_stack.value + "/" + name))
        elif self.secret_service == SecretService.SSM:
            l_secret = os.environ.get(name, self.get_ssm_param, name)

        if l_secret is not None:
            return l_secret
        else:
            return NO_VALUE_FOUND


def get_config():
    """
    Function to retrieve the global application config
    """
    global CONFIG # pylint: disable=global-statement
    if CONFIG is None:
        CONFIG = Config()
    return CONFIG
