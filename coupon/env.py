import dotenv

def init_env():
    dotenv.load_dotenv(dotenv.find_dotenv(
        usecwd=True,
        raise_error_if_not_found=True,
    ))
