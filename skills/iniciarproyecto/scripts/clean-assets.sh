#!/usr/bin/env bash
# Quita metadata de generadores IA (EXIF/XMP/C2PA/parámetros) de imágenes y video.
# Uso: clean-assets.sh <carpeta> [--in-place]
#   sin --in-place: escribe copias <nombre>.clean.<ext>
#   con --in-place: reemplaza el original y guarda backup en .assets-originales/
# Requiere: exiftool (imágenes) y/o ffmpeg (video). En Mac: brew install exiftool ffmpeg
# No quita logos visibles ni marcas invisibles (SynthID): eso requiere editar la imagen.
set -uo pipefail
dir="${1:-}"; inplace=0
[ "${2:-}" = "--in-place" ] && inplace=1
[ -d "$dir" ] || { echo "Uso: $0 <carpeta> [--in-place]"; exit 2; }
dir="${dir%/}"

have_exif=0; have_ff=0
command -v exiftool >/dev/null && have_exif=1
command -v ffmpeg >/dev/null && have_ff=1
[ $have_exif = 0 ] && echo "BLOQUEO parcial: falta exiftool, no proceso imágenes."
[ $have_ff = 0 ] && echo "BLOQUEO parcial: falta ffmpeg, no proceso video."

n=0; flagged=0
while IFS= read -r -d '' f; do
  case "$f" in *.clean.*|*/.assets-originales/*) continue ;; esac
  ext="${f##*.}"; lext="$(echo "$ext" | tr '[:upper:]' '[:lower:]')"
  if grep -aqiE 'c2pa|jumbf|"prompt"|parameters|Made with|DALL|Midjourney|Stable Diffusion|Gemini|Firefly' "$f" 2>/dev/null; then
    echo "huella   $f"; flagged=$((flagged + 1))
  fi
  out="${f%.*}.clean.$ext"
  case "$lext" in
    jpg|jpeg|png|webp|tif|tiff|heic|gif)
      [ $have_exif = 1 ] || continue
      cp "$f" "$out" && exiftool -q -all= -overwrite_original "$out" ;;
    mp4|mov|webm|m4v)
      [ $have_ff = 1 ] || continue
      ffmpeg -loglevel error -y -i "$f" -map_metadata -1 -map_chapters -1 -c copy "$out" ;;
    *) continue ;;
  esac
  if [ $inplace = 1 ]; then
    bak="$dir/.assets-originales/${f#"$dir"/}"; mkdir -p "$(dirname "$bak")"
    cp -p "$f" "$bak" && mv "$out" "$f"
    echo "limpio   $f (backup en $bak)"
  else
    echo "limpio   $out"
  fi
  n=$((n + 1))
done < <(find "$dir" -type f -print0)

echo
echo "clean-assets: $n archivos procesados · $flagged con huellas detectadas antes de limpiar."
