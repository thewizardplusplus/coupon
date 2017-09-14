import datetime
import urllib.parse
import functools

from . import consts
from . import logger

def process_coupons(coupons, processors):
    global_processor = compose(*processors)
    return (global_processor(coupon) for coupon in coupons)

def parse_dates(coupon):
    coupon['date_start'] = datetime.datetime.strptime(
        coupon['date_start'],
        consts.ADMITAD_TIMESTAMP_FORMAT,
    )
    coupon['date_end'] = datetime.datetime.strptime(
        coupon['date_end'],
        consts.ADMITAD_TIMESTAMP_FORMAT,
    )

    return coupon

def remove_i3_param(coupon):
    try:
        url = urllib.parse.urlparse(coupon['goto_link'])
        query = urllib.parse.parse_qs(url.query)
        if 'i' in query and query['i'] == ['3']:
            del query['i']

        coupon['goto_link'] = urllib.parse.urlunparse(urllib.parse.ParseResult(
            scheme=url.scheme,
            netloc=url.netloc,
            path=url.path,
            params=url.params,
            query=urllib.parse.urlencode(query),
            fragment=url.fragment,
        ))
    except Exception as exception:
        logger.get_logger().warning(exception)

    return coupon

# https://mathieularose.com/function-composition-in-python/
def compose(*functions):
    return functools.reduce(
        lambda f, g: lambda x: f(g(x)),
        functions,
        lambda x: x,
    )
