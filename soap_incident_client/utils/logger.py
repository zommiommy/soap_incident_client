import os
import sys
import logging

logger = logging.getLogger(__name__)
logging.addLevelName(logging.WARNING, 'WARN')

def setup_logger(log_level=logging.INFO):
    global logger
    logger.setLevel(log_level)
    
    formatter = logging.Formatter("%(levelname)s %(asctime)-15s %(message)s")

    shandler = logging.StreamHandler(sys.stdout)
    shandler.setLevel(log_level)
    shandler.setFormatter(formatter)
    logger.addHandler(shandler)