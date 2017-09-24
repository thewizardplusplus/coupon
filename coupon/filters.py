import os

import termcolor

from . import logger
from .script import parse
from .script import evaluate

def make_filter_by_script():
    if 'COUPON_SCRIPT' not in os.environ:
        return lambda coupon: True

    script_filename = os.environ['COUPON_SCRIPT']
    with open(script_filename, encoding='utf-8') as script_file:
        ast = parse.parse(script_file.read())

    logger.get_logger().info(
        'load the filter script ' + termcolor.colored(script_filename, 'green'),
    )

    return lambda coupon: evaluate.safe_evaluate(ast, coupon)

def make_filter_by_campaigns():
    required_campaigns = [
        campaign
        for campaign in os.environ.get('COUPON_CAMPAIGNS', '').split(',')
        for campaign in (campaign.strip(),)
        if len(campaign) != 0
    ]
    return lambda coupon: \
        coupon.get('campaign', {}).get('name', '').strip() in required_campaigns
