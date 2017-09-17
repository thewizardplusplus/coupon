import dotenv
import termcolor

from . import logger

def init_env():
    env_path = dotenv.find_dotenv(usecwd=True, raise_error_if_not_found=True)
    dotenv.load_dotenv(env_path)

    logger.get_logger().info(
        'load the %s config %s',
        termcolor.colored('.env', 'magenta'),
        termcolor.colored(env_path, 'green'),
    )
