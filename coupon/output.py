import os

def output_coupons(coupons):
    base_path = os.environ.get('OUTPUT_PATH', './coupons/')
    os.makedirs(base_path, exist_ok=True)

    for coupon in coupons:
        output_coupon(coupon, base_path)

def output_coupon(coupon, base_path):
    ...
