import sys

from . import logger
from . import env
from . import client
from . import db
from . import filters
from . import processors
from . import output

def main():
    logger.init_logger()

    try:
        env.init_env()

        client_obj = client.init_client()
        coupons = client.handle_pagination(client_obj, client.get_coupons)
        db_connection = db.init_db()
        coupons = filters.filter_coupons(db_connection, coupons)
        coupons = processors.process_coupons(coupons, [
            processors.parse_dates,
            processors.generate_final_link,
            processors.remove_i3_param,
            processors.make_campaigns_register(db_connection),
            processors.make_coupons_register(db_connection),
        ])
        output.output_coupons(coupons)
    except Exception as exception:
        logger.get_logger().error(exception)
        sys.exit(1)
    except KeyboardInterrupt:
        # output a line break after the ^C symbol in a terminal
        print('')

        sys.exit(1)
