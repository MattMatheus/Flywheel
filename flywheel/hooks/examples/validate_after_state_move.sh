#!/usr/bin/env bash
set -euo pipefail

./flywheel/tools/validate_workflow_state.sh --format json >/dev/null
