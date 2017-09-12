import os

from admitad import api
from admitad import items

def init_client():
    return api.get_oauth_client_client(
        os.environ['COUPON_ADMITAD_ID'],
        os.environ['COUPON_ADMITAD_SECRET'],
        ' '.join([items.CouponsForWebsite.SCOPE]),
    )

def get_coupons(client):
    return client.CouponsForWebsite.get(int(os.environ['COUPON_SITE_ID']))
