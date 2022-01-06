import logging
import logging.config
import yaml


def init_logging():
    with open("app/logging_config/config.yaml", "r") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    logger.info("Logger initialized from YAML file.")
    pass
