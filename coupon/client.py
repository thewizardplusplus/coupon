import os

from admitad import api
from admitad import items
from admitad import constants
import termcolor

from . import logger

def init_client():
    client = api.get_oauth_client_client(
        os.environ['COUPON_ADMITAD_ID'],
        os.environ['COUPON_ADMITAD_SECRET'],
        ' '.join([items.CouponsForWebsite.SCOPE]),
    )
    logger.get_logger().info(
        'init %s client',
        termcolor.colored('admitad', 'magenta'),
    )

    return client

def handle_pagination(client, requester):
    counter = 0
    offset = 0
    while True:
        response = requester(
            client,
            offset=offset,
            limit=constants.MAX_PAGINATION_LIMIT,
        )
        yield from response['results']

        counter = response['_meta']['count']
        offset += constants.MAX_PAGINATION_LIMIT
        if offset >= counter:
            break

def get_coupons(client, **kwargs):
    return client.CouponsForWebsite.get(
        int(os.environ['COUPON_SITE_ID']),
        **kwargs,
    )
