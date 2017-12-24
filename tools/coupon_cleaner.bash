#!/usr/bin/env bash

function log() {
  declare -r message="$1"

  echo "$(date --rfc-3339=ns) [INFO] $message" >&2
}

export $(grep -v '^#' .env | xargs)
declare current_timestamp="$(date +%s)"
for file in $(find "$COUPON_OUTPUT_PATH" -maxdepth 1 -type f -name *.html); do
  declare filename="$(basename "$file" .html)"
  declare coupon_id="$(echo "$filename" | cut -d_ -f3)"
  declare timestamp="$(echo "$filename" | cut -d_ -f2)"
  declare parsed_timestamp
  parsed_timestamp="$(date --date "$timestamp" +%s 2>/dev/null)"
  if [[ $? != 0 ]]; then
    continue
  fi

  if ((parsed_timestamp - current_timestamp < COUPON_TIMESTAMP_GAP)); then
    log "remove the coupon #$coupon_id"
    rm -f "$file"
  fi
done
