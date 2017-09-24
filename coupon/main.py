import sys

from . import logger
from . import env
from . import client
from . import filters
from . import processors
from . import output

def main():
    logger.init_logger()

    try:
        env.init_env()

        client_obj = client.init_client()
        coupons = client.handle_pagination(client_obj, client.get_coupons)
        filter_by_script = filters.make_filter_by_script()
        coupons = (
            coupon
            for coupon in coupons
            if filter_by_script(coupon)
        )
        coupons = processors.process_coupons(coupons, [
            processors.parse_dates,
            processors.remove_i3_param,
        ])
        output.output_coupons(coupons)
    except Exception as exception:
        logger.get_logger().error(exception)
        sys.exit(1)
    except KeyboardInterrupt:
        # output a line break after the ^C symbol in a terminal
        print('')

        sys.exit(1)
