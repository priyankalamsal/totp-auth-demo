#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="/data/backups"
mkdir -p "$BACKUP_DIR"

cp /data/seed.txt "$BACKUP_DIR/seed_$(date -u +%Y-%m-%d_%H-%M-%S).txt"

