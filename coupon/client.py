import os

from admitad import api

def init_client(*scopes):
    return api.get_oauth_client_client(
        os.environ['COUPON_ADMITAD_ID'],
        os.environ['COUPON_ADMITAD_SECRET'],
        ' '.join(set(scopes)),
    )
