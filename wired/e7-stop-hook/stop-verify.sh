#!/usr/bin/env bash
# Stop hook: blocks Claude from stopping if code was changed but not verified.
#
# Logic:
#   1. No uncommitted changes → allow stop (nothing to verify)
#   2. Changes exist + transcript shows build/test commands → allow stop
#   3. Changes exist + no verification evidence → block, inject verification prompt
#
# stdin: {"session_id": "...", "transcript_path": "..."}
# stdout: {} to allow, {"decision": "block", "reason": "..."} to block

set -euo pipefail

# Not in a git repo → nothing to verify
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  echo '{}'
  exit 0
fi

input=$(cat)
transcript_path=$(echo "$input" | jq -r '.transcript_path // ""')

# No changes → nothing to verify
if git diff --quiet HEAD 2>/dev/null && [ -z "$(git ls-files --others --exclude-standard 2>/dev/null)" ]; then
  echo '{}'
  exit 0
fi

# No build system in repo → nothing to verify (planning/docs repo)
repo_root=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -n "$repo_root" ]; then
  has_build=false
  for f in Cargo.toml package.json Makefile CMakeLists.txt pyproject.toml setup.py go.mod build.gradle pom.xml Gemfile; do
    if [ -f "$repo_root/$f" ]; then
      has_build=true
      break
    fi
  done
  if [ "$has_build" = false ]; then
    echo '{}'
    exit 0
  fi
fi

# Changes exist — check transcript for verification evidence
if [ -n "$transcript_path" ] && [ -f "$transcript_path" ]; then
  # Build/test commands ran
  if grep -qE 'cargo (test|build|clippy)|npm (test|run build)|pytest|vitest|jest|make test|go test' "$transcript_path"; then
    echo '{}'
    exit 0
  fi
  # Non-code session declared (breaks the loop for read-only sessions)
  if grep -qE '[Nn]on-code session' "$transcript_path"; then
    echo '{}'
    exit 0
  fi
fi

# Changes exist, no verification found — block and request verification
cat <<'STOP'
{
  "decision": "block",
  "reason": "You have uncommitted code changes but no build/test verification was detected in this session. Before stopping, run the project's build and test commands to verify your changes compile and pass. If this is a non-code session (research, planning), say so and stop again."
}
STOP
exit 0
