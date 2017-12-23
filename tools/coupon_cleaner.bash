#!/usr/bin/env bash

export $(grep -v '^#' .env | xargs)
for file in $(find "$COUPON_OUTPUT_PATH" -maxdepth 1 -type f -name *.html); do
  declare filename="$(basename "$file" .html)"
  declare timestamp="$(echo "$filename" | cut -d_ -f2)"
  declare coupon_id="$(echo "$filename" | cut -d_ -f3)"
  echo "filename: \"$filename\""
  echo "timestamp: \"$timestamp\""
  echo "coupon ID: \"$coupon_id\""
done
