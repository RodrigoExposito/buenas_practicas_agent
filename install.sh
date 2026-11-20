#!/usr/bin/env bash
# Instala el kit /iniciarproyecto en ~/.claude
# Uso: ./install.sh [--dry-run]
# Si un archivo existe y difiere, se guarda una copia <archivo>.bak-<fecha> antes de reemplazarlo.
set -euo pipefail
cd "$(dirname "$0")"

dry=0
[ "${1:-}" = "--dry-run" ] && dry=1
dest="${CLAUDE_HOME:-$HOME/.claude}"
stamp="$(date +%Y%m%d-%H%M%S)"
installed=0; backed=0; same=0

copy() { # copy <origen> <destino>
  local src="$1" dst="$2"
  if [ -f "$dst" ] && cmp -s "$src" "$dst"; then same=$((same + 1)); return; fi
  if [ $dry = 1 ]; then
    [ -f "$dst" ] && echo "reemplazaría (con backup) $dst" || echo "crearía      $dst"
    return
  fi
  mkdir -p "$(dirname "$dst")"
  if [ -f "$dst" ]; then cp -p "$dst" "$dst.bak-$stamp"; backed=$((backed + 1)); fi
  cp -p "$src" "$dst"
  installed=$((installed + 1))
}

for dir in skills agents commands; do
  while IFS= read -r -d '' f; do
    copy "$f" "$dest/${f#./}"
  done < <(find "./$dir" -type f ! -path '*/__pycache__/*' ! -name '*.pyc' ! -name '.DS_Store' -print0)
done

if [ $dry = 0 ]; then
  chmod +x "$dest"/skills/iniciarproyecto/scripts/*.sh "$dest"/skills/iniciarproyecto/scripts/*.py \
           "$dest"/skills/iniciarproyecto/templates/githooks/* 2>/dev/null || true
fi

echo
echo "Kit /iniciarproyecto v2 → $dest"
echo "  nuevos o actualizados: $installed · sin cambios: $same · backups: $backed"
[ $backed -gt 0 ] && echo "  (backups con sufijo .bak-$stamp)"

missing=""
for bin in git python3 node npx; do command -v "$bin" >/dev/null || missing="$missing $bin"; done
[ -n "$missing" ] && echo "  AVISO: faltan en el sistema:$missing"
for bin in exiftool ffmpeg; do command -v "$bin" >/dev/null || echo "  opcional: $bin (para clean-assets.sh)"; done

cat <<'EOF'

Siguiente:
  1. Reiniciá Claude Code.
  2. Verificá con /agents → arquitecto, programador, verificador.
  3. En un repo: /iniciarproyecto <tu idea>
EOF
