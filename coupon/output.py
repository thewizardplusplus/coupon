import re
import locale
import os

import jinja2

from . import logger
from . import consts

PARAGRAPH_PATTERN = re.compile(r'\r\n|\n\r|\n|\r')
SENTENCE_PATTERN = re.compile(r'\.(?:\W|$)')

def output_coupons(coupons):
    # sets the locale setting for the datetime.strptime() function
    locale.setlocale(locale.LC_ALL, (
        os.environ.get('COUPON_LOCALE', 'en_US'),
        'UTF-8',
    ))

    mode = os.environ.get('COUPON_OUTPUT_MODE', 'FILES')
    if mode not in ['FILES', 'STDOUT']:
        raise Exception('incorrect output mode ' + mode)

    base_path = None
    if mode == 'FILES':
        base_path = os.environ.get('COUPON_OUTPUT_PATH', './coupons/')
        os.makedirs(base_path, exist_ok=True)

    with open(os.environ['COUPON_TEMPLATE'], encoding='utf-8') as template_file:
        environment = jinja2.Environment(autoescape=False)
        environment.filters['format_timestamp'] = format_timestamp
        environment.filters['cut'] = cut
        environment.filters['to_paragraphs'] = to_paragraphs

        template = environment.from_string(template_file.read())

    for coupon in coupons:
        if mode == 'FILES':
            output_coupon_to_file(coupon, template, base_path)
        elif mode == 'STDOUT':
            output_coupon_to_stdout(coupon, template)

def output_coupon_to_file(coupon, template, base_path):
    try:
        with open(os.path.join(
            base_path,
            'coupon_{}.html'.format(coupon['id']),
        ), mode='w', encoding='utf-8') as coupon_file:
            coupon_file.write(format_coupon(coupon, template))
    except Exception as exception:
        logger.get_logger().warning(exception)

def output_coupon_to_stdout(coupon, template):
    print(format_coupon(coupon, template))

def format_coupon(coupon, template):
    return template.render(coupon=coupon)

def format_timestamp(timestamp, format_=consts.ADMITAD_TIMESTAMP_FORMAT):
    return timestamp.strftime(format_)

def cut(text, cut_mark):
    first_paragraph, *rest_text = PARAGRAPH_PATTERN.split(
        text.strip(),
        maxsplit=1,
    )
    first_sentence, *rest_paragraph = SENTENCE_PATTERN.split(
        first_paragraph,
        maxsplit=1,
    )
    text_parts = [
        sentence
        for sentence in [first_sentence, *rest_paragraph, *rest_text]
        for sentence in (sentence.strip(),)
        if len(sentence) != 0
    ]
    return '\n'.join(
        text_parts[:1] + [cut_mark] + text_parts[1:] \
            if len(text_parts) > 1 \
            else text_parts
    )

def to_paragraphs(text, cut_mark=''):
    return '\n'.join(
        '<p>{}</p>'.format(paragraph) \
            if len(cut_mark) == 0 or paragraph != cut_mark \
            else cut_mark
        for paragraph in PARAGRAPH_PATTERN.split(text.strip())
    )
