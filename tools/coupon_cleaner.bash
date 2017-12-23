#!/usr/bin/env bash

export $(grep -v '^#' .env | xargs)
echo "$COUPON_OUTPUT_PATH"
echo "$COUPON_TIMESTAMP_GAP"
