#!/usr/bin/env bash
# Registra el estado actual en SYNC.md y lista qué docs re-subir al Project de Claude.
# Uso: claude-sync-update.sh [--commit] [--fase "Fase C — Listado de facturas"] [--log "texto de la sesión"]
set -euo pipefail
root="$(git rev-parse --show-toplevel)"
cd "$root"

commit=0; fase=""; log=""
while [ $# -gt 0 ]; do
  case "$1" in
    --commit) commit=1 ;;
    --fase) fase="$2"; shift ;;
    --log) log="$2"; shift ;;
    -h|--help) sed -n '2,3p' "$0"; exit 0 ;;
    *) echo "opción desconocida: $1"; exit 2 ;;
  esac
  shift
done

[ -f SYNC.md ] || { echo "No existe SYNC.md"; exit 1; }

prev="$(awk '/<!-- sync:head -->/{f=1;next} /<!-- \/sync:head -->/{f=0} f' SYNC.md | sed -n 's/^head: *//p')"
head="$(git rev-parse --short HEAD)"
now="$(date '+%Y-%m-%d %H:%M')"
[ -z "$fase" ] && [ -f ROADMAP.md ] && fase="$(grep -m1 '^## \[~\]' ROADMAP.md | sed 's/^## \[~\] *//' || true)"

python3 - "$head" "$now" "${fase:-(ninguna)}" "$log" <<'PY'
import re, sys
head, now, fase, log = sys.argv[1:5]
src = open("SYNC.md", encoding="utf-8").read()
def put(text, name, body):
    pat = re.compile(rf"(<!-- sync:{name} -->\n)(.*?)(<!-- /sync:{name} -->)", re.S)
    return pat.sub(lambda m: m.group(1) + body + "\n" + m.group(3), text, count=1)
src = put(src, "head", f"head: {head}\nupdated: {now}")
src = put(src, "fase", fase)
if log:
    src = src.rstrip("\n") + f"\n- {now[:10]} · {log}\n"
open("SYNC.md", "w", encoding="utf-8").write(src)
PY

echo "SYNC.md: head=$head · fase=${fase:-(ninguna)}"

# Qué re-subir al Project
manifest="scripts/sync-manifest.txt"
if [ -f "$manifest" ] && [ -n "$prev" ] && git cat-file -e "$prev^{commit}" 2>/dev/null; then
  changed="$(git diff --name-only "$prev" HEAD)"
  echo "Re-subir al Project de Claude (cambiaron desde $prev):"
  found=0
  while IFS= read -r pat; do
    case "$pat" in ''|'#'*) continue ;; esac
    while IFS= read -r f; do
      [ -n "$f" ] && case "$f" in $pat) echo "  - $f"; found=1 ;; esac
    done <<< "$changed"
  done < "$manifest"
  [ "$found" = 0 ] && echo "  (nada)"
fi

if [ "$commit" = 1 ]; then
  git add SYNC.md
  if git diff --cached --quiet -- SYNC.md; then
    echo "SYNC.md sin cambios para commitear."
  else
    git commit -m "chore(sync): update session state" -- SYNC.md >/dev/null
    echo "Commit: $(git log -1 --format='%h %s')"
  fi
fi
