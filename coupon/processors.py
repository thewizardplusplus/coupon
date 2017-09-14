import datetime
import functools

ADMITAD_TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S'

def process_coupons(coupons, processors):
    global_processor = compose(*processors)
    return (global_processor(coupon) for coupon in coupons)

def parse_dates(coupon):
    coupon['date_start'] = datetime.datetime.strptime(
        coupon['date_start'],
        ADMITAD_TIMESTAMP_FORMAT,
    )
    coupon['date_end'] = datetime.datetime.strptime(
        coupon['date_end'],
        ADMITAD_TIMESTAMP_FORMAT,
    )

    return coupon

# https://mathieularose.com/function-composition-in-python/
def compose(*functions):
    return functools.reduce(
        lambda f, g: lambda x: f(g(x)),
        functions,
        lambda x: x,
    )