# app/config.py

import os
from datetime import timedelta


class Config:
    """Base configuration for the Flask application"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Snowflake connection configuration
    SNOWFLAKE_USER = 'Ankur'
    SNOWFLAKE_PASSWORD = 'bTJawBrXFJb4VyE'
    SNOWFLAKE_ACCOUNT = 'ut20337.ap-southeast-1'
    SNOWFLAKE_DATABASE = 'TRIAL_DB'
    SNOWFLAKE_SCHEMA = 'TRIAL_SCMA'
    SNOWFLAKE_WAREHOUSE = 'compute_wh'
    SNOWFLAKE_ROLE = 'ACCOUNTADMIN'

    # Snowflake connection string with error handling
    try:
        SQLALCHEMY_DATABASE_URI = (
            'snowflake://{user}:{password}@{account}/{database}/{schema}?'
            'warehouse={warehouse}&role={role}'
        ).format(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
            warehouse=SNOWFLAKE_WAREHOUSE,
            role=SNOWFLAKE_ROLE
        )
    except Exception as e:
        raise Exception(
            f"Failed to create Snowflake connection string: {str(e)}")


class DevelopmentConfig(Config):
    """Configuration for development environment"""
    DEBUG = True


class ProductionConfig(Config):
    """Configuration for production environment"""
    DEBUG = False


class TestingConfig(Config):
    """Configuration for testing environment"""
    TESTING = True


# Select the right configuration based on environment
config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)
