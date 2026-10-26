#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$ROOT"
fail=0
# Heuristic only; this does not replace a proper secret scanner or human review.
if grep -RInE --exclude-dir=.git --exclude='SECURITY.md' --exclude='check_repo_hygiene.sh' '(AKIA[0-9A-Z]{16}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})' .; then
  echo "Possible credential/private-key pattern found; inspect before publishing." >&2
  fail=1
fi
if find . -type f \( -name '*.pem' -o -name '*.key' -o -name '.env' -o -name '*.p12' -o -name '*.pfx' \) -print | grep .; then
  echo "Potential secret file exists in the working tree." >&2
  fail=1
fi
if [[ "$fail" -ne 0 ]]; then exit 1; fi
echo "Basic hygiene checks passed; this heuristic is not a complete secret scanner."
