import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger for the given module name. Uses structured formatting suitable for ingestion pipelines.

    Args:
        name (str): The name of the module

    Returns:
        logging.Logger: Logger helper
    """
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger