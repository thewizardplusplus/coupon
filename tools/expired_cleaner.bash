#!/usr/bin/env bash

function log() {
  declare -r level="$1"
  declare -r message="$2"

  echo "$(date --rfc-3339=ns) [$level] $message" >&2
}

function get_segment() {
  declare -r text="$1"
  declare -ri number=$2

  echo "$text" | cut -d_ -f$number
}

export $(grep -v '^#' .env | xargs)
log INFO "load the .env config $(realpath .env)"

declare -r output_path="${COUPON_OUTPUT_PATH:-./coupons/}"
declare -r coupons="$(find "$output_path" -maxdepth 1 -type f -name *.html)"
log INFO "find $(echo -n "$coupons" | wc -l) coupons"

declare -ri timestamp_gap="${COUPON_TIMESTAMP_GAP:-0}"
declare -ri current_timestamp="$(date +%s)"
for coupon in $coupons; do
  declare filename="$(basename "$coupon" .html)"
  declare coupon_id="$(get_segment "$filename" 3)"
  declare timestamp="$(get_segment "$filename" 2)"
  declare parsed_timestamp
  parsed_timestamp="$(date --date "$timestamp" +%s 2>/dev/null)"
  if [[ $? != 0 ]]; then
    declare coupon_id="$(get_segment "$filename" 2)"
    log WARNING "coupon #$coupon_id has an incorrect timestamp"

    continue
  fi

  if ((parsed_timestamp - current_timestamp < timestamp_gap)); then
    log INFO "remove the coupon #$coupon_id"
    rm -f "$coupon"
  fi
done
