import logging
import logging.config
import yaml


def init_prod_logging():
    with open("app/logging_config/prod_config.yaml", "r") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    logger.info("Production logger initialized from YAML file.")
    pass


def init_dev_logging():
    with open("app/logging_config/dev_config.yaml", "r") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    logger = logging.getLogger("__name__")
    logger.info("Development logger initialized from YAML file.")
    pass
