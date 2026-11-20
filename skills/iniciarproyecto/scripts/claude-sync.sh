#!/usr/bin/env bash
# Brief de inicio de sesión. Lo corre el hook SessionStart; su salida entra sola al contexto.
# Nunca falla: si algo no está, lo dice.
root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$root" || exit 0

block() { # block <archivo> <nombre>: contenido entre <!-- sync:nombre --> y <!-- /sync:nombre -->
  [ -f "$1" ] && awk -v s="<!-- sync:$2 -->" -v e="<!-- /sync:$2 -->" '$0==e{f=0} f{print} $0==s{f=1}' "$1"
}
section() { # section <archivo> <título>: líneas bajo "## título" hasta el próximo "## "
  [ -f "$1" ] && awk -v t="## $2" '$0 ~ "^## " {f = ($0 == t); next} f && NF {print}' "$1" | grep -v '^<!--' | head -n "${3:-8}"
}

name="$(basename "$root")"
branch="$(git branch --show-current 2>/dev/null || echo '?')"
head="$(git rev-parse --short HEAD 2>/dev/null || echo 'sin commits')"

echo "=== BRIEF: $name ==="
echo "rama: $branch · HEAD: $head"

# Estado de sync
reg="$(block SYNC.md head | sed -n 's/^head: *//p')"
upd="$(block SYNC.md head | sed -n 's/^updated: *//p')"
if [ ! -f SYNC.md ]; then
  echo "sync: SIN SYNC.md (correr /iniciarproyecto o crear desde la plantilla)"
elif [ -z "$reg" ] || [ "$reg" = "(sin registrar)" ]; then
  echo "sync: sin HEAD registrado"
elif git cat-file -e "$reg^{commit}" 2>/dev/null; then
  changed="$(git diff --name-only "$reg" HEAD 2>/dev/null | grep -v '^SYNC.md$' || true)"
  if [ -z "$changed" ]; then
    echo "sync: OK (registrado $reg, $upd)"
  else
    n=$(echo "$changed" | wc -l | tr -d ' ')
    echo "sync: MISMATCH — $n archivos cambiaron desde $reg ($upd). Leé el log de SYNC.md antes de seguir."
  fi
else
  echo "sync: HEAD registrado $reg no existe en este clon"
fi

dirty="$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
[ "${dirty:-0}" != "0" ] && echo "cambios sin commitear: $dirty archivos"

# Fase
fase="$(block SYNC.md fase | grep -v '^(ninguna)$' | head -n 3)"
[ -z "$fase" ] && [ -f ROADMAP.md ] && fase="$(grep -m1 '^## \[~\]' ROADMAP.md | sed 's/^## //')"
next="$( [ -f ROADMAP.md ] && grep -m1 '^## \[ \]' ROADMAP.md | sed 's/^## //')"
echo "fase activa: ${fase:-ninguna}"
echo "siguiente: ${next:-roadmap completo o sin ROADMAP.md}"

pend="$(section SYNC.md Pendientes 6 | grep -v '^- *$')"
[ -n "$pend" ] && { echo "pendientes:"; echo "$pend"; }
notas="$(section SYNC.md Notas 4 | grep -v '^- *$')"
[ -n "$notas" ] && { echo "notas:"; echo "$notas"; }

# Flujos críticos
if [ -f scripts/critical-flows.py ] && [ -f docs/ARCHITECTURE.md ]; then
  python3 scripts/critical-flows.py summary 2>/dev/null
fi

last="$( [ -f SYNC.md ] && grep -E '^- ?[0-9]{4}-' SYNC.md | tail -n 1)"
[ -n "$last" ] && echo "última sesión: $last"

echo "reglas: una fase por sesión · evidencia antes de 'listo' · bloqueos se declaran · sin push"
echo "=== /retomar para el detalle ==="
exit 0
