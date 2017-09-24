import os

import termcolor

from . import logger
from . import db
from .script import parse
from .script import evaluate

def filter_coupons(db_connection, coupons):
    filter_by_campaigns = make_filter_by_campaigns()
    filter_by_database = make_filter_by_database(db_connection)
    filter_by_script = make_filter_by_script()
    for coupon in coupons:
        try:
            if filter_by_campaigns(coupon) \
                or (filter_by_database(coupon) and filter_by_script(coupon)):
                yield coupon
        except Exception as exception:
            logger.get_logger().warning(exception)

def make_filter_by_script():
    if 'COUPON_SCRIPT' not in os.environ:
        return lambda coupon: True

    script_filename = os.environ['COUPON_SCRIPT']
    with open(script_filename, encoding='utf-8') as script_file:
        ast = parse.parse(script_file.read())

    logger.get_logger().info(
        'load the filter script ' + termcolor.colored(script_filename, 'green'),
    )

    return lambda coupon: evaluate.evaluate_or_expression(ast, coupon)

def make_filter_by_campaigns():
    required_campaigns = [
        campaign
        for campaign in os.environ.get('COUPON_CAMPAIGNS', '').split(',')
        for campaign in (campaign.strip(),)
        if len(campaign) != 0
    ]
    return lambda coupon: \
        coupon['campaign']['name'].strip() in required_campaigns

def make_filter_by_database(db_connection):
    if db_connection is None:
        return lambda coupon: True

    number = abs(int(os.environ.get('COUPON_NUMBER', '1')))
    interval = abs(int(os.environ.get('COUPON_INTERVAL', str(24 * 60 * 60))))
    return lambda coupon: number >= db.count_registered_campaigns(
        db_connection,
        coupon['campaign']['name'].strip(),
        interval,
    )
