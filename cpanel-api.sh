#!/usr/bin/env bash
# ============================================================
#  Appel de l'API cPanel (UAPI) avec le jeton de .deploy.env.
#
#  Usage :  ./cpanel-api.sh 'VersionControl/retrieve'
#           ./cpanel-api.sh 'VersionControl/update?repository_root=...&branch=main'
#
#  Le jeton ne passe jamais par la ligne de commande.
# ============================================================
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[ -f "$HERE/.deploy.env" ] || { echo "✗ .deploy.env absent (voir .deploy.env.exemple)"; exit 1; }
. "$HERE/.deploy.env"

: "${CPANEL_USER:?CPANEL_USER manquant dans .deploy.env}"
: "${CPANEL_TOKEN:?CPANEL_TOKEN manquant dans .deploy.env}"
: "${CPANEL_HOST:=server173-3.web-hosting.com}"

[ $# -ge 1 ] || { echo "Usage : $0 'Module/fonction?param=...' [options curl supplémentaires]"; exit 1; }

ENDPOINT="$1"; shift
curl --silent --show-error --max-time 120 \
     -H "Authorization: cpanel ${CPANEL_USER}:${CPANEL_TOKEN}" \
     "$@" \
     "https://${CPANEL_HOST}:2083/execute/$ENDPOINT"
