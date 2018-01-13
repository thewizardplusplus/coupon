#!/usr/bin/env bash

export $(grep -v '^#' .env | xargs)
declare -r output_path="${COUPON_OUTPUT_PATH:-./coupons/}"
declare -r database="${COUPON_DATABASE:-./coupon.db}"
echo "output path: $output_path"
echo "database: $database"
