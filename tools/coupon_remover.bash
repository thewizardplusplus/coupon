#!/usr/bin/env bash

function log() {
  declare -r level="$1"
  declare -r message="$2"

  echo "$(date --rfc-3339=ns) [$level] $message" >&2
}

export $(grep -v '^#' .env | xargs)
declare -r output_path="${COUPON_OUTPUT_PATH:-./coupons/}"
declare -r database="${COUPON_DATABASE:-./coupon.db}"
for file in $(find "$output_path" -maxdepth 1 -type f -name *.html); do
  declare -i coupon_id="$(basename "$file" .html | awk -F_ '{print $NF}')"
  log INFO "remove the coupon #$coupon_id from the database"
  sqlite3 -bail "$database" "
    DELETE FROM coupons WHERE coupon_id = $coupon_id
  " 2>/dev/null
  if [[ $? != 0 ]]; then
    log WARNING "unable to remove the coupon #$coupon_id from the database"
    continue
  fi

  log INFO "remove the coupon #$coupon_id from files"
  rm -f "$file"
done
