import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler


LOGGING_CONFIG = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'standard': {
			'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
			}
		},
	'handlers': {
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'standard'
			},
		'file': {
			'level': 'DEBUG',
			'class': 'logging.handlers.TimedRotatingFileHandler',
			'filename': 'app.log',
			'formatter': 'standard',
			'when': 'midnight',
			'interval': 1,
			'backupCount': 7,
			}
		},
	'loggers': {
		'': {
			'handlers': ['console', 'file'],
			'level': 'DEBUG',
			'propagate': True
			}
		}
	}

# Call it ones in __init__.py
def setup_logging():
	logging.config.dictConfig(LOGGING_CONFIG)


# Example of use

# import logging
# from log_config import setup_logging # only for __init__.py
"""
setup_logging() # only in __init__.py

logger = logging.getLogger(__name__)

logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
"""
