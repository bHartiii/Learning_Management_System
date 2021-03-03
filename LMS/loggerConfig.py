import logging
import os
from celery.signals import after_setup_logger

file_name = "Logs/LMS.log"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

logging.basicConfig(filename=file_name, level=logging.INFO, filemode='w',
                    format="%(asctime)s:%(levelname)s:%(message)s")
log = logging.getLogger()

@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] - %(message)s')

    log = logging.FileHandler('Logs/celery.log')
    log.setFormatter(formatter)
    logger.addHandler(log)
