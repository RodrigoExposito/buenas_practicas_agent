---
description: Cierra la sesión - log, lecciones del entorno, SYNC.md commiteado, qué re-subir
---

1. Resumí la sesión en una línea: `fase · resultado · próximo paso`.
2. Actualizá `SYNC.md` a mano si cambió algo en **Pendientes** o **Notas** (borrá lo resuelto).
3. **Lecciones del entorno.** Repasá la sesión y buscá fricciones causadas por el entorno, no por el código:
   - el agente necesitó contexto que no estaba en AGENTS.md o en una skill,
   - repitió un error que una regla habría evitado,
   - un permiso, la red o un MCP lo bloqueó o lo confundió,
   - leyó el mismo archivo muchas veces o un tool devolvió salidas enormes,
   - dijo que algo funcionaba y no era cierto.
   Por cada una, proponé **un cambio concreto** (línea en AGENTS.md, regla en una skill `convenciones-*`, permiso en `.claude/settings.json`, hook, quitar un MCP) y mostralo como diff.
   **Esperá aprobación** antes de aplicarlo. Lo aprobado se aplica y se registra en `docs/HARNESS.md`.
   Si no hubo fricciones, decí "sin lecciones de entorno" y no inventes.
4. Si la sesión fue larga o pesada, sugerí `/auditarsesion` antes de cerrar.
5. Corré `bash scripts/claude-sync-update.sh --log "<línea del paso 1>" --commit`.
   Si quedaron cambios de docs/harness sin commitear, primero `/commit`.
6. Mostrá:
   - la lista "Re-subir al Project de Claude" que imprime el script,
   - `git log --oneline @{u}..HEAD 2>/dev/null || git log --oneline -5` (lo que falta pushear),
   - el recordatorio: **`git push` lo hacés vos**, después `/clear` antes de la próxima fase.
