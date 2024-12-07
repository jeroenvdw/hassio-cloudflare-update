#!/usr/bin/with-contenv bashio

API_TOKEN=$(bashio::config 'api_token')
ZONE_ID=$(bashio::config 'zone_id')
DOMAIN=$(bashio::config 'domain')
SLEEP_TIME=$(bashio::config 'sleep_time')

python3 /update_dns_record.py  "${API_TOKEN}" "${ZONE_ID}" "${DOMAIN}" "${SLEEP_TIME}"