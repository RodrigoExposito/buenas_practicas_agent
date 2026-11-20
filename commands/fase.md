---
description: Implementa la siguiente fase - programador, verificador, prueba humana, commit
argument-hint: "[letra o nombre de fase; vacío = la siguiente pendiente]"
---

Ejecutá UNA fase del roadmap. Fase pedida: `$ARGUMENTS` (si está vacío, la primera `[ ]` de `ROADMAP.md`).

## 1. Preparar
- Marcá la fase como `[~]` en `ROADMAP.md` y corré `bash scripts/claude-sync-update.sh --fase "<nombre de la fase>"`.
- Mostrá en 3 líneas: objetivo, archivos, flujos críticos que toca.

## 2. Implementar
Delegá al subagente **programador** con este encargo:
> Implementá la fase "<nombre>" de ROADMAP.md siguiendo AGENTS.md y las skills convenciones-* que apliquen. TDD. Si toca CF-xx, el test crítico va primero. Devolvé el resumen obligatorio con salidas reales y bloqueos.

Si el programador reporta **BLOQUEOS**, frená y mostralos al humano antes de seguir.

## 3. Verificar
Delegá al subagente **verificador** (contexto limpio, sin el razonamiento del programador):
> Verificá la fase "<nombre>" de ROADMAP.md contra sus criterios de aceptación. Informe en el formato fijo.

- **RECHAZADA** → volvé al paso 2 con el informe (máximo 2 vueltas; a la tercera, `/rescate`).
- **NO VERIFICABLE** → mostrale al humano qué falta (acceso, datos, servicio) y esperá.
- **APROBADA** → seguí.

## 4. Gate de flujos críticos
Corré `python3 scripts/critical-flows.py check --strict` solo sobre los CF que toca la fase y `python3 scripts/critical-flows.py run`.
Si algún CF de esta fase falla o no tiene test, la fase **no cierra**.

## 5. Prueba humana
Mostrá la sección "Para el humano" del informe del verificador como checklist y **esperá confirmación explícita**.
No avances con un "dale" ambiguo si el checklist tenía puntos: pedí que confirme que los probó.

## 6. Cerrar
- Marcá la fase `[x]` en `ROADMAP.md`.
- Corré `/commit`.
- Sugerí `/cerrarsesion`.
