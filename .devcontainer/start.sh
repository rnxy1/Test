#!/usr/bin/env bash
set -Eeuo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
FRAPPE_DOCKER_DIR="$REPO_ROOT/.runtime/frappe_docker"

if [ ! -f "$FRAPPE_DOCKER_DIR/pwd.yml" ]; then
  echo "Frappe Docker runtime is missing. Run: bash .devcontainer/setup.sh"
  exit 1
fi

echo "==> Starting the disposable Marley demo stack"
docker compose \
  -p marley-demo \
  -f "$FRAPPE_DOCKER_DIR/pwd.yml" \
  -f "$REPO_ROOT/.devcontainer/compose.override.yml" \
  up -d

echo
echo "============================================================"
echo "Marley demo is starting."
echo "Open forwarded port 8080 in Codespaces."
echo "Login: Administrator"
echo "Password: admin"
echo
echo "Frappe / ERPNext / Marley Desk: /app"
echo "Marley Frontend:              /healthcare"
echo "============================================================"
