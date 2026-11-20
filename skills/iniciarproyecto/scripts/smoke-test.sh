#!/usr/bin/env bash
# Smoke post-deploy: verifica status HTTP (y texto opcional) de las rutas de smoke.txt.
# Uso: smoke-test.sh <base-url> [archivo]   ej: smoke-test.sh https://mi-app.vercel.app
set -uo pipefail
base="${1:-}"; file="${2:-smoke.txt}"
[ -z "$base" ] && { echo "Uso: $0 <base-url> [smoke.txt]"; exit 2; }
[ -f "$file" ] || { echo "No existe $file"; exit 2; }
command -v curl >/dev/null || { echo "BLOQUEO: curl no está instalado"; exit 2; }
base="${base%/}"

fail=0; total=0
while read -r path expected needle; do
  case "$path" in ''|'#'*) continue ;; esac
  total=$((total + 1))
  body="$(mktemp)"
  code="$(curl -sS -L -o "$body" -w '%{http_code}' --max-time 20 "$base$path" 2>/dev/null)"
  rc=$?
  if [ $rc -ne 0 ] || [ "$code" = "000" ]; then
    echo "BLOQUEO  $path  sin respuesta (curl rc=$rc). ¿Red, DNS o URL incorrecta?"
    fail=$((fail + 1))
  elif [ "$code" != "$expected" ]; then
    echo "FALLA    $path  esperado $expected, obtuve $code"
    fail=$((fail + 1))
  elif [ -n "${needle:-}" ] && ! grep -qi -- "$needle" "$body"; then
    echo "FALLA    $path  $code pero no aparece '$needle'"
    fail=$((fail + 1))
  else
    echo "ok       $path  $code"
  fi
  rm -f "$body"
done < "$file"

echo
echo "smoke: $((total - fail))/$total ok contra $base"
[ $fail -eq 0 ]
