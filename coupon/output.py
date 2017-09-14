import locale
import os

import jinja2

from . import logger
from . import consts

def output_coupons(coupons):
    # sets the locale setting for the datetime.strptime() function
    locale.setlocale(locale.LC_ALL, (
        os.environ.get('COUPON_LOCALE', 'en_US'),
        'UTF-8',
    ))

    base_path = os.environ.get('COUPON_OUTPUT_PATH', './coupons/')
    os.makedirs(base_path, exist_ok=True)

    with open(os.environ['COUPON_TEMPLATE'], encoding='utf-8') as template_file:
        environment = jinja2.Environment(autoescape=True)
        environment.filters['format_timestamp'] = format_timestamp

        template = environment.from_string(template_file.read())

    for coupon in coupons:
        output_coupon(coupon, base_path, template)

def output_coupon(coupon, base_path, template):
    try:
        with open(os.path.join(
            base_path,
            'coupon_{}.html'.format(coupon['id']),
        ), mode='x', encoding='utf-8') as coupon_file:
            coupon_file.write(format_coupon(coupon, template))
    except Exception as exception:
        logger.get_logger().warning(exception)

def format_coupon(coupon, template):
    return template.render(coupon=coupon)

def format_timestamp(timestamp, format_=consts.ADMITAD_TIMESTAMP_FORMAT):
    return timestamp.strftime(format_)
