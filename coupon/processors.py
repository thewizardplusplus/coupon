import functools

def process_coupons(coupons, processors):
    global_processor = compose(*processors)
    return (global_processor(coupon) for coupon in coupons)

# https://mathieularose.com/function-composition-in-python/
def compose(*functions):
    return functools.reduce(
        lambda f, g: lambda x: f(g(x)),
        functions,
        lambda x: x,
    )
