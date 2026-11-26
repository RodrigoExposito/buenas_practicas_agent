#!/usr/bin/env bash
# Hook PostToolUse (Edit|Write): formatea y chequea el archivo recién editado.
#
# Lee por stdin el JSON que manda Claude Code y usa tool_input.file_path.
# Solo corre las herramientas que el proyecto ya tiene instaladas; si no hay ninguna, no hace nada.
#   exit 0  sin problemas (o nada que correr)
#   exit 2  quedan errores en ese archivo: van por stderr para que el agente los corrija
#
# Variables:
#   POST_EDIT_TSC=0   saltea el chequeo de tipos (útil si tsc tarda demasiado en el proyecto)
set -u

root="${CLAUDE_PROJECT_DIR:-$(pwd)}"

file="$(python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
    print((data.get("tool_input") or {}).get("file_path") or "")
except Exception:
    print("")
' 2>/dev/null)"

[ -n "$file" ] || exit 0
case "$file" in /*) ;; *) file="$root/$file" ;; esac
[ -f "$file" ] || exit 0

case "$file" in "$root"/*) ;; *) exit 0 ;; esac
rel="${file#"$root"/}"
case "/$rel" in
  */node_modules/*|*/.next/*|*/dist/*|*/build/*|*/out/*|*/coverage/*|*/.git/*) exit 0 ;;
esac

cd "$root" || exit 0
bin="node_modules/.bin"
problems=""

note() { # note <herramienta> <salida>
  problems="${problems}
--- $1 ---
$2"
}

has_eslint_config() {
  local f
  for f in eslint.config.* .eslintrc .eslintrc.*; do
    [ -f "$f" ] && return 0
  done
  return 1
}

case "$rel" in
  *.ts|*.tsx|*.js|*.jsx|*.mjs|*.cjs)
    if [ -x "$bin/prettier" ]; then
      out="$("$bin/prettier" --write --log-level warn "$rel" 2>&1)" || note "prettier" "$out"
    fi
    if [ -x "$bin/eslint" ] && has_eslint_config; then
      out="$("$bin/eslint" --fix "$rel" 2>&1)" || note "eslint" "$out"
    fi
    ;;
  *.json|*.css|*.scss)
    if [ -x "$bin/prettier" ]; then
      out="$("$bin/prettier" --write --log-level warn "$rel" 2>&1)" || note "prettier" "$out"
    fi
    ;;
  *.py)
    # Los hooks heredan el PATH del shell, no el del entorno virtual del proyecto.
    ruff=""
    if [ -x .venv/bin/ruff ]; then ruff=".venv/bin/ruff"; elif command -v ruff >/dev/null 2>&1; then ruff="ruff"; fi
    if [ -n "$ruff" ]; then
      out="$("$ruff" format "$rel" 2>&1)" || note "ruff format" "$out"
      # Imports y variables sin usar se reportan pero no se borran solos: el agente suele
      # agregar el import en una edición y usarlo en la siguiente.
      out="$("$ruff" check --fix --unfixable F401,F841 "$rel" 2>&1)" || note "ruff check" "$out"
    fi
    ;;
esac

# Tipos: tsc revisa el proyecto entero, pero solo se reportan los errores del archivo editado.
# Los errores en otros archivos los atrapa el paso de lint/types del ciclo de la fase.
case "$rel" in
  *.ts|*.tsx)
    if [ "${POST_EDIT_TSC:-1}" != "0" ] && [ -x "$bin/tsc" ] && [ -f tsconfig.json ]; then
      out="$("$bin/tsc" --noEmit --pretty false 2>&1 | grep -F "$rel(" || true)"
      [ -n "$out" ] && note "tsc" "$out"
    fi
    ;;
esac

if [ -n "$problems" ]; then
  {
    echo "post-edit: quedan problemas en $rel. Corregilos antes de seguir."
    echo "$problems"
  } >&2
  exit 2
fi
exit 0
