#!/usr/bin/env bash
set -euo pipefail

REPO_OWNER="Bigibaba2"
REPO_NAME="Okira22"
PKG_VERSION="1.0.0-controlled-launch"
PKG_NAME="okira22_${PKG_VERSION}_all.deb"
DOWNLOAD_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}/releases/download/v${PKG_VERSION}/${PKG_NAME}"
TMP_DEB="/tmp/${PKG_NAME}"

fail() {
  echo "[okira22-installer] ERROR: $1" >&2
  exit 1
}

info() {
  echo "[okira22-installer] $1"
}

require_linux() {
  uname -s | grep -qi linux || fail "Linux is required"
}

require_root() {
  [ "$(id -u)" -eq 0 ] || fail "Run this installer with sudo"
}

require_tools() {
  command -v curl >/dev/null 2>&1 || fail "curl is required"
  command -v apt >/dev/null 2>&1 || fail "apt is required"
  command -v dpkg >/dev/null 2>&1 || fail "dpkg is required"
}

download_package() {
  info "Downloading ${PKG_NAME}"
  rm -f "$TMP_DEB"
  curl -fL "$DOWNLOAD_URL" -o "$TMP_DEB" || fail "Package download failed"
  [ -s "$TMP_DEB" ] || fail "Downloaded package is empty"
}

install_package() {
  info "Installing package"
  apt update
  apt install -y "$TMP_DEB" || fail "Package install failed"
}

validate_install() {
  info "Validating install"
  command -v okira22 >/dev/null 2>&1 || fail "okira22 CLI not found after install"

  okira22 status >/dev/null || fail "okira22 status failed"
  okira22 controlled-launch-truth >/dev/null || fail "okira22 controlled-launch-truth failed"
  okira22 pre-launch-smoke >/dev/null || fail "okira22 pre-launch-smoke failed"
}

finish() {
  info "Okira22 installed successfully"
  echo
  echo "Next commands:"
  echo "  okira22 status"
  echo "  okira22 controlled-launch-truth"
  echo "  okira22 pre-launch-smoke"
}

main() {
  require_linux
  require_root
  require_tools
  download_package
  install_package
  validate_install
  finish
}

main "$@"
