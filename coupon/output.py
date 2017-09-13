import os

import jinja2

def output_coupons(coupons):
    base_path = os.environ.get('COUPON_OUTPUT_PATH', './coupons/')
    os.makedirs(base_path, exist_ok=True)

    with open(os.environ['COUPON_TEMPLATE'], encoding='utf-8') as template_file:
        template = jinja2.Template(template_file.read())

    for coupon in coupons:
        output_coupon(coupon, base_path, template)

def output_coupon(coupon, base_path, template):
    with open(os.path.join(
        base_path,
        'coupon_{}.html'.format(coupon['id']),
    ), mode='x', encoding='utf-8') as coupon_file:
        coupon_file.write(format_coupon(coupon, template))

def format_coupon(coupon, template):
    return template.render(coupon=coupon)
