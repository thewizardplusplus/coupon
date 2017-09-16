import os

from .script import parse
from .script import evaluate

def filter_coupons_by_script(coupons):
    if 'COUPON_SCRIPT' not in os.environ:
        return coupons

    with open(os.environ['COUPON_SCRIPT'], encoding='utf-8') as script_file:
        ast = parse.parse(script_file.read())

    return (
        coupon
        for coupon in coupons
        if evaluate.safe_evaluate(ast, coupon)
    )
