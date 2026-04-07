#!/usr/bin/env bash
# Mock deploy status checker for Wired E16 demo.
# Passes on checks 1-2, fails on check 3+ (simulates a deploy failure).

COUNTER_FILE="/tmp/deploy_check_counter"

# Initialize or increment counter
if [[ -f "$COUNTER_FILE" ]]; then
    count=$(cat "$COUNTER_FILE")
    count=$((count + 1))
else
    count=1
fi
echo "$count" > "$COUNTER_FILE"

echo "=== Deploy Status Check #$count ==="
echo "Timestamp: $(date '+%H:%M:%S')"
echo ""

if [[ $count -le 2 ]]; then
    echo "Service: api-gateway     [RUNNING]"
    echo "Service: auth-service    [RUNNING]"
    echo "Service: user-service    [RUNNING]"
    echo ""
    echo "All services healthy."
    exit 0
else
    echo "Service: api-gateway     [RUNNING]"
    echo "Service: auth-service    [FAILING]"
    echo "Service: user-service    [RUNNING]"
    echo ""
    echo "ERROR: auth-service health check failed"
    echo "Last error: connection refused on port 8443"
    exit 1
fi
