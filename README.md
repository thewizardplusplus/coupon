# Coupon

Utility for a getting and a formatting of coupons from the [admitad](https://www.admitad.com/) service.

## Features

- log in an [admitad](https://www.admitad.com/) account;
- getting of a coupon list for a specific website;
- filter a coupon list:
  - filter by a script in the microlanguage (see below for details);
  - disable a filtering for specified campaigns;
  - via a remembering in an SQLite database:
    - limit a frequency of coupons with same campaigns;
    - skip coupons that were previously processed;
- output a coupon list:
  - format an output:
    - format an output with an Jinja2 template;
    - Jinja2 template extensions:
      - format a timestamp;
      - flatten a text (replace line breaks with a specific string);
      - extract a cut (first sentence) with a specific cut mark;
      - split a text to paragraphs with a specific paragraph format (optionally skip a specific cut mark);
  - output target may be:
    - separate files;
    - stdout.

## Installation

Clone this repository:

```
$ git clone https://github.com/thewizardplusplus/coupon.git
$ cd coupon
```

Then install the utility with [pip](https://pip.pypa.io/) tool:

```
$ sudo -H python3.5 -m pip install .
```

`sudo` command is required to install `coupon` console script. If it's not required, `sudo` command can be omitted:

```
$ python3.5 -m pip install .
```

But then the utility should be started as `python3.5 -m coupon`.

## Usage

```
$ coupon
```

Environment variables:

- `COUPON_ADMITAD_ID` &mdash; ID of the Admitad app;
- `COUPON_ADMITAD_SECRET` &mdash; secret of the Admitad app;
- `COUPON_SITE_ID` &mdash; ID of the site;
- `COUPON_OUTPUT_PATH` &mdash; path for output coupons (default: `./coupons/`);
- `COUPON_TEMPLATE` &mdash; path to the coupon template (default: `./docs/rich_coupon_template.example.html`);
- `COUPON_LOCALE` &mdash; locale for timestamp formatting (default: `ru_RU`);
- `COUPON_SCRIPT` &mdash; path to the filter script (default: `./docs/coupon_script.example.00.coupon`);
- `COUPON_OUTPUT_MODE` &mdash; mode of output coupons (default: `FILES|STDOUT`);
- `COUPON_CAMPAIGNS` &mdash; comma-separated list of disabled campaigns (default: `Domino's Pizza, Связной, Юлмарт`);
- `COUPON_DATABASE` &mdash; path to the SQLite database (default: `./coupon.db`);
- `COUPON_NUMBER` &mdash; allowed count of coupons with same campaigns (default: `1`);
- `COUPON_INTERVAL` &mdash; time window for restriction of coupons with same campaigns (default: `86400`).

Environment variables can be specified in a `.env` config in the format:

```
NAME_1=value_1
NAME_2=value_2
...
```

See details about the format: https://github.com/motdotla/dotenv#rules.

A `.env` config will never modify any environment variables that have already been set.

## Microlanguage Grammar

[Microlanguage grammar](docs/microlanguage_grammar.md).

## License

The MIT License (MIT)

Copyright &copy; 2017-2018 thewizardplusplus
