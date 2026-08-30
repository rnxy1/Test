#!/usr/bin/env bash
set -Eeuo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
RUNTIME_DIR="$REPO_ROOT/.runtime"
FRAPPE_DOCKER_DIR="$RUNTIME_DIR/frappe_docker"
IMAGE_NAME="marley-demo:v16"

mkdir -p "$RUNTIME_DIR"

echo "==> Preparing official Frappe Docker tooling"
if [ ! -d "$FRAPPE_DOCKER_DIR/.git" ]; then
  rm -rf "$FRAPPE_DOCKER_DIR"
  git clone --depth 1 https://github.com/frappe/frappe_docker.git "$FRAPPE_DOCKER_DIR"
else
  git -C "$FRAPPE_DOCKER_DIR" fetch --depth 1 origin main
  git -C "$FRAPPE_DOCKER_DIR" reset --hard origin/main
fi

echo "==> Building one image containing Frappe v16 + ERPNext v16 + Marley Health v16 + Marley Frontend"
if ! docker image inspect "$IMAGE_NAME" >/dev/null 2>&1; then
  (
    cd "$FRAPPE_DOCKER_DIR"
    DOCKER_BUILDKIT=1 docker build \
      --secret "id=apps_json,src=$REPO_ROOT/.devcontainer/apps.json" \
      --build-arg FRAPPE_BRANCH=version-16 \
      --build-arg FRAPPE_PATH=https://github.com/frappe/frappe \
      --tag "$IMAGE_NAME" \
      --file images/layered/Containerfile \
      .
  )
else
  echo "==> $IMAGE_NAME already exists; skipping rebuild"
fi

bash "$REPO_ROOT/.devcontainer/start.sh"
