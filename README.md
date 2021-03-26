# flask_utils

a set of utils to facilitate the development and deployment of a flask api running in docker, with AWS ECR and ECS

## Purpose and intended audience 

For use in creating a Flask RESTful API following the pattern (essentially) established by AAIS during the migration away
from MuleSoft. This set of utils allows a user to concentrate on writing the endpoints of the Flask API, supplying essential
functionality for DB connection, configuration handling, logging, and app setup, as well as Slack integration. For more 
detail on how to integrate these, see example apps:

* https://github.huit.harvard.edu/HUIT/adexutilsecs-app-flask-simple-api
* https://github.huit.harvard.edu/HUIT/adexutilsecs-app-flask-sqlalchemy-api

## Requirements

    python >=3.7

## Installation

Within an appropriate python virtual environment:

    pip install https://github.com/huit/flask_utils/archive/refs/tags/v0.0.1.tar.gz#egg=adex-flask-utils    

## Usage

Several utils are exposed as objects; others offer useful methods:
```
api_util.py
* get_api()
* setup_api()
* configure_app()
* cleanup()

db_util.py
* DB_UTIL
    for db operations. see https://github.com/huit/pydb for more details on available methods
    
config_util.py    
* CONFIG_UTIL
    for accessing configuration. see https://github.com/huit/pyconfig for more details
    
logger_util.py    
* get_common_logger - for creating loggers for a python file/class according to a common pattern
* add_pre_post - adds logging pre- and post- request

monitor_health.py
    2 endpoints of use for confirming app functionality:
    "/monitor/health" verifies DB connectivity
    "/monitor/hello/<string:title>/<string:message>" verifies slack integration
  
security_util.py
* api_key_required() - wraps a method that represents an endpoint to ensure that the request has the proper api key 
* api_endpoint_exception_handling() wraps an api endpoint method to provide basic exception handling   
```

## Examples

* https://github.huit.harvard.edu/HUIT/adexutilsecs-app-flask-simple-api
* https://github.huit.harvard.edu/HUIT/adexutilsecs-app-flask-sqlalchemy-api