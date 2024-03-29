import os
import pathlib
import logging

class BaseConfig:  # 基本配置
    LOG_DIR = os.path.join(os.path.dirname(__file__), '../logs')
    LOG_FILENAME = 'app.log'
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True

class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
