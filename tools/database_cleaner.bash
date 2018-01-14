#!/usr/bin/env bash

function log() {
  declare -r level="$1"
  declare -r message="$2"

  echo "$(date --rfc-3339=ns) [$level] $message" >&2
}

export $(grep -v '^#' .env | xargs)
log INFO "load the .env config $(realpath .env)"

declare -r output_path="${COUPON_OUTPUT_PATH:-./coupons/}"
declare -r coupons="$(find "$output_path" -maxdepth 1 -type f -name '*.html')"
log INFO "find $(echo -n "$coupons" | wc -l) coupons"

declare -r database="${COUPON_DATABASE:-./coupon.db}"
for coupon in $coupons; do
  declare -i coupon_id="$(basename "$coupon" .html | awk -F_ '{print $NF}')"
  log INFO "remove the coupon #$coupon_id from the database"
  sqlite3 -bail "$database" "
    DELETE FROM coupons WHERE coupon_id = $coupon_id
  " 2>/dev/null
  if [[ $? != 0 ]]; then
    log WARNING "unable to remove the coupon #$coupon_id from the database"
    continue
  fi

  log INFO "remove the coupon #$coupon_id from files"
  rm -f "$coupon"
done
