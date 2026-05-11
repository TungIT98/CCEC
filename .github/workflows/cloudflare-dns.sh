#!/bin/bash
# Cloudflare DNS update via GitHub Actions (IP-restricted token workaround)
# This script runs in CI where the token IP policy was configured

set -e

CLOUDFLARE_TOKEN="${{ secrets.CLOUDFLARE_API_TOKEN }}"
ZONE_NAME="${CLOUDFLARE_ZONE:-example.com}"
SUBDOMAIN="${CLOUDFLARE_SUBDOMAIN:-ccec}"
TARGET_HOST="${CF_TARGET_HOST:-ccec-web.fly.dev}"

echo "=== Cloudflare DNS Setup ==="
echo "Zone: $ZONE_NAME"
echo "Subdomain: $SUBDOMAIN"
echo "Target: $TARGET_HOST"

# Step 1: Find zone ID
ZONE_RESPONSE=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=$ZONE_NAME" \
  -H "Authorization: Bearer $CLOUDFLARE_TOKEN" \
  -H "Content-Type: application/json")

ZONE_ID=$(echo "$ZONE_RESPONSE" | node -e "const d=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')); console.log(d.result && d.result[0] ? d.result[0].id : 'NOT_FOUND')")

if [ "$ZONE_ID" = "NOT_FOUND" ]; then
  echo "Zone $ZONE_NAME not found. Create it at dash.cloudflare.com first, then add CLOUDFLARE_ZONE secret."
  echo "Zone Response: $ZONE_RESPONSE"
  exit 0
fi

echo "Zone ID: $ZONE_ID"

# Step 2: Check if CNAME record exists
DNS_RESPONSE=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?type=CNAME&name=$SUBDOMAIN.$ZONE_NAME" \
  -H "Authorization: Bearer $CLOUDFLARE_TOKEN" \
  -H "Content-Type: application/json")

echo "DNS Records Response: $DNS_RESPONSE"

# Check if record exists
RECORD_ID=$(echo "$DNS_RESPONSE" | node -e "const d=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')); console.log(d.result && d.result[0] ? d.result[0].id : 'NONE')")

if [ "$RECORD_ID" != "NONE" ]; then
  echo "Record exists ($RECORD_ID), updating..."
  # Update existing record
  curl -s -X PUT "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
    -H "Authorization: Bearer $CLOUDFLARE_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"type\":\"CNAME\",\"name\":\"$SUBDOMAIN\",\"content\":\"$TARGET_HOST\",\"proxied\":true,\"ttl\":3600}" | node -e "const d=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')); console.log('Updated:', d.success, d.result ? d.result.name : d.errors)"
else
  echo "Record does not exist, creating..."
  # Create new record
  curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
    -H "Authorization: Bearer $CLOUDFLARE_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"type\":\"CNAME\",\"name\":\"$SUBDOMAIN\",\"content\":\"$TARGET_HOST\",\"proxied\":true,\"ttl\":3600}" | node -e "const d=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')); console.log('Created:', d.success, d.result ? d.result.name : d.errors)"
fi

echo "=== Cloudflare DNS setup complete ==="
echo "DNS should propagate in ~5 minutes. Set CLOUDFLARE_ZONE secret in GitHub repo."