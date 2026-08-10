#!/usr/bin/env bash
# Reconstruit dist/ et le zip prêt à téléverser, à partir des sources.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
python3 build-langs.py
rm -rf dist sevrage-tunisie-site.zip
mkdir -p dist/assets
cp index.html ar.html en.html 404.html .htaccess robots.txt sitemap.xml dist/
cp -R assets/css assets/js assets/fonts assets/img assets/logo dist/assets/
rm -f dist/assets/fonts/all.css dist/assets/logo/README.md
find dist -name '.DS_Store' -delete
( cd dist && zip -qr ../sevrage-tunisie-site.zip . )
echo "dist/ : $(find dist -type f | wc -l | tr -d ' ') fichiers — zip : $(du -h sevrage-tunisie-site.zip | cut -f1)"
