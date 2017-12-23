#!/usr/bin/env bash

export $(grep -v '^#' .env | xargs)
declare current_timestamp="$(date +%s)"
for file in $(find "$COUPON_OUTPUT_PATH" -maxdepth 1 -type f -name *.html); do
  declare filename="$(basename "$file" .html)"
  declare coupon_id="$(echo "$filename" | cut -d_ -f3)"
  declare timestamp="$(echo "$filename" | cut -d_ -f2)"
  declare parsed_timestamp="$(date --date "$timestamp" +%s)"
  echo "current timestamp:$current_timestamp"
  echo "parsed timestamp: $parsed_timestamp"
  if ((parsed_timestamp - current_timestamp < COUPON_TIMESTAMP_GAP)); then
    echo "remove file $file"
  fi
done
