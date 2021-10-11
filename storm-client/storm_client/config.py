#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Configuration options for SpatioTemporal Open Research Manager."""

import os

_BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_settings(env):
    """Get the given enviroment configuration."""
    return CONFIG.get(env)

class Config:
    """Base Configuration."""

    DEBUG = False
    TESTING = False

    SECRET_KEY = 'secret-key'

    STORM_CLIENT_BASE_PATH_TEMPLATES = os.getenv('STORM_CLIENT_BASE_PATH_TEMPLATES', 'templates')

    STORM_CLIENT_SMTP_PORT = os.getenv('STORM_CLIENT_SMTP_PORT', 587)
    STORM_CLIENT_SMTP_HOST = os.getenv('STORM_CLIENT_SMTP_HOST', None)

    STORM_CLIENT_EMAIL_ADDRESS = os.getenv('STORM_CLIENT_EMAIL_ADDRESS', None)
    STORM_CLIENT_EMAIL_PASSWORD = os.getenv('STORM_CLIENT_EMAIL_PASSWORD', None)

    STORM_CLIENT_APM_APP_NAME = os.environ.get('BDC_AUTH_APM_APP_NAME', None)
    STORM_CLIENT_APM_HOST = os.environ.get('BDC_AUTH_APM_HOST', None)
    STORM_CLIENT_APM_SECRET_TOKEN = os.environ.get('BDC_AUTH_APM_SECRET_TOKEN', None)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:postgres@localhost:5432/storm_client')

    OAUTH2_REFRESH_TOKEN_GENERATOR = True

    # Default OAuth 2.0 client app for Brazil Data Cube
    STORM_CLIENT_DEFAULT_APP = 'bdc-auth'

    # Base path used in production (with proxy)
    APPLICATION_ROOT = os.getenv('STORM_CLIENT_PREFIX', '/')
    SESSION_COOKIE_PATH = os.getenv('SESSION_COOKIE_PATH', '/')

    # Logstash configuration
    BDC_LOGSTASH_URL = os.getenv('BDC_LOGSTASH_URL', 'localhost')
    BDC_LOGSTASH_PORT = os.getenv('BDC_LOGSTASH_PORT', 5044)


class ProductionConfig(Config):
    """Production Mode."""


class DevelopmentConfig(Config):
    """Development Mode."""

    DEVELOPMENT = True


class TestingConfig(Config):
    """Testing Mode (Continous Integration)."""

    TESTING = True
    DEBUG = True


CONFIG = {
    "DevelopmentConfig": DevelopmentConfig(),
    "ProductionConfig": ProductionConfig(),
    "TestingConfig": TestingConfig()
}