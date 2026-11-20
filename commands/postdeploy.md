---
description: Verificación post-deploy - smoke HTTP + recorrido del flujo principal en producción
argument-hint: "<url de producción>"
---

URL: `$ARGUMENTS`. Si está vacía, pedila (no la adivines).

1. **Smoke HTTP:** `bash scripts/smoke-test.sh $ARGUMENTS`. Mostrá la salida completa.
   Cualquier línea `BLOQUEO` (sin red, DNS) se reporta como tal: no es ni OK ni falla del deploy.
2. **Recorrido real** con el subagente **verificador**:
   > Contra $ARGUMENTS (producción, solo lectura): recorré los flujos críticos de docs/ARCHITECTURE.md que no modifiquen datos reales, en desktop y en móvil (390×844). Revisá consola y requests fallidos. Capturas. No crees, edites ni borres datos de producción; si un flujo lo requiere, marcalo NO VERIFICADO y dale los pasos al humano.
3. Informe:
   ```
   PRODUCCIÓN: <url> · <fecha>
   Smoke: <n/n ok>
   Flujos: <CF-xx: OK | FALLA | NO VERIFICADO>
   Consola/red: <...>
   Veredicto: SANO | DEGRADADO | CAÍDO
   ```
4. Si está DEGRADADO o CAÍDO: proponé `/rescate` con el síntoma y, si el deploy anterior estaba sano, recordá cómo hacer rollback en el proveedor (lo ejecuta el humano).
5. Registrá una línea en el log de `SYNC.md` con `bash scripts/claude-sync-update.sh --log "postdeploy <veredicto> <url>"`.
