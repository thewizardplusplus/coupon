#!/usr/bin/env bash

export $(grep -v '^#' .env | xargs)
for file in $(find "$COUPON_OUTPUT_PATH" -maxdepth 1 -type f -name *.html); do
  echo "\"$file\""
done
