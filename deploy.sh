#!/usr/bin/env bash
# ============================================================
#  Envoi du site vers Namecheap Stellar, par FTPS.
#
#  Le mot de passe est demandé au lancement : jamais écrit sur
#  le disque, jamais dans l'historique du shell.
#
#  Usage :  ./deploy.sh
# ============================================================
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/dist"

[ -d "$SRC" ] || { echo "✗ dist/ est absent. Lancez d'abord :  ./package.sh"; exit 1; }

[ -f "$HERE/.deploy.env" ] && . "$HERE/.deploy.env"

# L'hôte doit être le NOM DU SERVEUR cPanel, pas le domaine :
# le certificat FTPS est émis pour le serveur. cPanel → Server Information.
FTP_HOST_DEFAULT="server173-3.web-hosting.com"
: "${FTP_HOST:=$FTP_HOST_DEFAULT}"
: "${FTP_USER:=}"
: "${FTP_DIR:=/public_html}"
: "${FTP_INSECURE:=0}"

while :; do
  read -rp "Hôte FTP        [$FTP_HOST] : " a; [ -n "$a" ] && FTP_HOST="$a"
  case "$FTP_HOST" in
    *@*) echo "  ✗ Ceci est un identifiant, pas un serveur. Laissez vide pour"
         echo "    utiliser $FTP_HOST_DEFAULT — c'est le nom couvert par le certificat."
         FTP_HOST="$FTP_HOST_DEFAULT" ;;
      *) break ;;
  esac
done
[ -n "$FTP_USER" ] || read -rp "Identifiant FTP (nom@sevrage-tunisie.com) : " FTP_USER
read -rsp "Mot de passe (masqué)         : " FTP_PASS; echo
echo

SSLOPT=(--ssl-reqd)
[ "$FTP_INSECURE" = "1" ] && SSLOPT+=(--insecure)

# ── 1 · connexion, puis on trouve tout seul la racine du site ──
echo "→ test de connexion sur $FTP_USER@$FTP_HOST …"

try_ls () { curl --silent --show-error --fail "${SSLOPT[@]}" \
              --user "$FTP_USER:$FTP_PASS" --list-only "ftp://$FTP_HOST$1/" 2>&1; }

if ! root=$(try_ls "/"); then
  echo "✗ Connexion refusée."
  echo "  $root"
  echo
  recovered=0

  case "$root" in
    *certificate*|*SSL*|*TLS*)
      echo "  → Le certificat FTPS est émis pour le serveur, pas pour ce nom."
      if [ "$FTP_HOST" != "$FTP_HOST_DEFAULT" ]; then
        echo "  → Nouvel essai sur $FTP_HOST_DEFAULT …"
        FTP_HOST="$FTP_HOST_DEFAULT"
        if root=$(try_ls "/"); then recovered=1; echo "  ✓ ça passe sur le nom du serveur."; fi
      fi
      if [ "$recovered" = 0 ]; then
        echo
        echo "  La liaison resterait chiffrée, mais l'identité du serveur ne"
        echo "  serait pas vérifiée. Sur votre réseau c'est acceptable ; sur un"
        echo "  wifi public, préférez cPanel → File Manager."
        read -rp "  Réessayer sans vérifier le certificat ? [o/N] : " yn
        case "$yn" in
          [oOyY]*) SSLOPT=(--ssl-reqd --insecure)
                   if root=$(try_ls "/"); then recovered=1; echo "  ✓ connecté."
                   else echo "  ✗ $root"; fi ;;
        esac
      fi ;;

    *530*|*login*|*"Access denied"*)
      echo "  → Identifiant ou mot de passe refusé. Pour un compte créé dans"
      echo "    cPanel → FTP Accounts, l'identifiant s'écrit en entier :"
      echo "    sevrageboss@sevrage-tunisie.com" ;;

    *)
      echo "  → Port 21 filtré ? Passez par cPanel → File Manager et"
      echo "    téléversez sevrage-tunisie-site.zip." ;;
  esac

  if [ "$recovered" != 1 ]; then unset FTP_PASS; exit 1; fi
fi

# Un compte FTP secondaire est cloisonné : /public_html n'existe pas pour lui,
# sa racine EST déjà le dossier du site. On regarde ce qu'on voit.
if printf '%s\n' "$root" | grep -qx "public_html"; then
  FTP_DIR="/public_html"
elif printf '%s\n' "$root" | grep -qxE "index\.html|assets|404\.html|cgi-bin"; then
  FTP_DIR=""
else
  echo "  Contenu de la racine :"
  printf '%s\n' "$root" | sed 's/^/    /' | head -12
  read -rp "  Dossier cible (vide = ici même) [$FTP_DIR] : " a
  FTP_DIR="${a:-$FTP_DIR}"
  [ "$FTP_DIR" = "/" ] && FTP_DIR=""
fi
echo "→ destination : ${FTP_DIR:-la racine du compte}"
echo "✓ connexion établie."
echo

# ── 2 · envoi ───────────────────────────────────────────────
# Certains serveurs cPanel refusent le transfert (451, 425) selon le mode
# de connexion de données. On cherche le mode qui passe sur le premier
# fichier, puis on garde celui-là pour les cinquante autres.
MODES=("" "--disable-epsv" "--ftp-skip-pasv-ip" "--disable-epsv --ftp-skip-pasv-ip" "--ftp-ssl-ccc")
MODE=""; MODE_FOUND=0

put () { # $1 = fichier local, $2 = chemin distant, $3… = options
  local f="$1" rel="$2"; shift 2
  curl --silent --show-error --fail "${SSLOPT[@]}" $* \
       --ftp-create-dirs --user "$FTP_USER:$FTP_PASS" \
       --upload-file "$f" "ftp://$FTP_HOST$FTP_DIR/$rel" 2>&1
}

total=$(find "$SRC" -type f | wc -l | tr -d ' ')
sent=0; failed=0; i=0

while IFS= read -r -d '' f; do
  rel="${f#"$SRC"/}"; i=$((i+1))

  if [ "$MODE_FOUND" = 0 ]; then
    for m in "${MODES[@]}"; do
      if err=$(put "$f" "$rel" $m); then
        MODE="$m"; MODE_FOUND=1
        [ -n "$m" ] && echo "  ↻ mode de transfert retenu : $m"
        break
      fi
    done
    if [ "$MODE_FOUND" = 0 ]; then
      echo "✗ Aucun mode de transfert ne passe."
      echo "  Dernière erreur : $err"
      echo
      echo "  Un 451 vient presque toujours du serveur, pas de vous :"
      echo "    • quota du compte FTP épuisé → cPanel → FTP Accounts → Quota"
      echo "    • dossier en lecture seule   → cPanel → File Manager → Permissions (755)"
      echo
      echo "  Le plus rapide reste cPanel → File Manager :"
      echo "    téléversez sevrage-tunisie-site.zip puis clic droit → Extract."
      unset FTP_PASS; exit 1
    fi
    sent=$((sent+1)); printf "  [%2d/%d] ✓ %s\n" "$i" "$total" "$rel"
    continue
  fi

  if err=$(put "$f" "$rel" $MODE); then
    sent=$((sent+1)); printf "  [%2d/%d] ✓ %s\n" "$i" "$total" "$rel"
  else
    failed=$((failed+1)); printf "  [%2d/%d] ✗ %s — %s\n" "$i" "$total" "$rel" "$err" >&2
  fi
done < <(find "$SRC" -type f -print0)

unset FTP_PASS
echo
echo "Terminé : $sent envoyé(s), $failed échec(s)."
[ "$failed" -eq 0 ] || exit 1

cat <<'NEXT'

⚠️  Supprimez la page de parking laissée par Namecheap dans public_html
    (default.html, index.php, cgi-bin/ …) sinon elle peut masquer le site.

Ensuite, dans cPanel :
  1. SSL/TLS Status → Run AutoSSL
  2. Email Accounts → Create → contact@psychiatrie-sevrage.com
  3. Ouvrir https://sevrage-tunisie.com
NEXT
