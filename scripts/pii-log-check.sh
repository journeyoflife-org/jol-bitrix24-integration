#!/usr/bin/env bash
# pii-log-check.sh — Scan log files for potential PII leaks.
#
# Searches application and audit logs for patterns that indicate
# personal data may have been written to logs in violation of the
# PII-safe logging policy.
#
# Usage: ./scripts/pii-log-check.sh [log_directory]
set -euo pipefail

LOG_DIR="${1:-/var/log/jol-bitrix24}"
EXIT_CODE=0

echo "=== PII Log Scan ==="
echo "Directory: $LOG_DIR"
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%S%z)"
echo ""

if [ ! -d "$LOG_DIR" ]; then
    echo "[WARN] Log directory does not exist: $LOG_DIR"
    echo "[INFO] Nothing to scan."
    exit 0
fi

# Patterns that indicate PII
declare -A PATTERNS=(
    ["Email"]='[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    ["Phone"]="\\+?[0-9][0-9[:space:]-()]{7,}[0-9]"
    ["Street_Address"]='[0-9]{1,5}[[:space:]]+[A-Za-z]+[[:space:]]+(Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b'
)

TOTAL_FILES=$(find "$LOG_DIR" -name "*.log" -o -name "*.jsonl" | wc -l)
echo "Found $TOTAL_FILES log file(s) to scan."
echo ""

for pattern_name in "${!PATTERNS[@]}"; do
    pattern="${PATTERNS[$pattern_name]}"
    echo "--- Checking: $pattern_name ---"

    MATCHES=$(grep -rn -E "$pattern" "$LOG_DIR" --include="*.log" --include="*.jsonl" 2>/dev/null || true)

    if [ -n "$MATCHES" ]; then
        echo "[FAIL] Potential PII found for pattern '$pattern_name':"
        echo "$MATCHES" | head -20
        EXIT_CODE=1
    else
        echo "[PASS] No matches for '$pattern_name'"
    fi
    echo ""
done

# Check that ***REDACTED*** appears (confirms filter is active)
REDACTED_COUNT=$(grep -r "\*\*\*REDACTED\*\*\*" "$LOG_DIR" --include="*.log" 2>/dev/null | wc -l || echo "0")
echo "Redaction markers found: $REDACTED_COUNT"

echo ""
if [ "$EXIT_CODE" -eq 0 ]; then
    echo "=== PASS: No PII detected in log files ==="
else
    echo "=== FAIL: Potential PII detected — review required ==="
fi

exit "$EXIT_CODE"
