import sys

from . import logger
from . import env

def main():
    logger.init_logger()

    try:
        env.init_env()
    except Exception as exception:
        logger.get_logger().error(exception)
        sys.exit(1)
    except KeyboardInterrupt:
        # output a line break after the ^C symbol in a terminal
        print('')

        sys.exit(1)
