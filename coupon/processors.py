import datetime
import urllib.parse
import functools

from . import consts
from . import logger
from . import db

def process_coupons(coupons, processors):
    global_processor = compose(*processors)
    for coupon in coupons:
        try:
            yield global_processor(coupon)
        except Exception as exception:
            logger.get_logger().warning(exception)

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

    return coupon

def make_campaigns_register(db_connection):
    def campaigns_register(coupon):
        db.register_campaign(db_connection, coupon['campaign']['name'])
        return coupon

    return campaigns_register

# https://mathieularose.com/function-composition-in-python/
def compose(*functions):
    return functools.reduce(
        lambda f, g: lambda x: f(g(x)),
        functions,
        lambda x: x,
    )
