import os

def output_coupons(coupons):
    base_path = os.environ.get('OUTPUT_PATH', './coupons/')
    os.makedirs(base_path, exist_ok=True)

    for coupon in coupons:
        output_coupon(coupon, base_path)

def output_coupon(coupon, base_path):
    with open(os.path.join(
        base_path,
        'coupon_{}.html'.format(coupon['id']),
    ), mode='x', encoding='utf-8') as coupon_file:
        coupon_file.write(format_coupon(coupon))

def format_coupon(coupon):
    return 'test\n'
