#!/usr/bin/env bash

export $(grep -v '^#' .env | xargs)
declare -r output_path="${COUPON_OUTPUT_PATH:-./coupons/}"
declare -r database="${COUPON_DATABASE:-./coupon.db}"
for file in $(find "$output_path" -maxdepth 1 -type f -name *.html); do
  declare -i coupon_id="$(basename "$file" .html | awk -F_ '{print $NF}')"
  echo "coupon ID: $coupon_id"
done
