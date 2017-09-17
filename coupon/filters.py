import os

import termcolor

from . import logger
from .script import parse
from .script import evaluate

def filter_coupons_by_script(coupons):
    if 'COUPON_SCRIPT' not in os.environ:
        return coupons

    script_filename = os.environ['COUPON_SCRIPT']
    with open(script_filename, encoding='utf-8') as script_file:
        ast = parse.parse(script_file.read())

    logger.get_logger().info(
        'load the filter script ' + termcolor.colored(script_filename, 'green'),
    )

    return (
        coupon
        for coupon in coupons
        if evaluate.safe_evaluate(ast, coupon)
    )
