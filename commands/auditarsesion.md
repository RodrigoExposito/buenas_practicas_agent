---
description: Observabilidad - dónde se fue el contexto, qué tools pesan, qué abaratar
argument-hint: "[--last N]"
model: sonnet
---

1. Corré el reporte (usa el script del proyecto si existe, si no el global):
   `python3 scripts/session-report.py $ARGUMENTS 2>/dev/null || python3 ~/.claude/skills/iniciarproyecto/scripts/session-report.py $ARGUMENTS`
   Si devuelve BLOQUEO, explicá la causa y terminá.
2. Explicá el reporte en lenguaje simple, en no más de 8 líneas:
   - cuánto contexto se usó y si hubo riesgo de degradación (pico > 60%),
   - qué tool o MCP se llevó la mayor parte del volumen y por qué,
   - si la caché se aprovechó.
3. Convertí cada recomendación en un **cambio concreto** al entorno (no al código de producto):
   quitar un MCP de `.mcp.json`, resumir un archivo muy leído en `AGENTS.md` o en una skill, acotar salidas con un script, partir fases grandes.
4. Mostralos como diff y esperá aprobación. Lo aprobado va a `docs/HARNESS.md`.

Nota: esto lee las transcripciones locales de Claude Code. Para métricas centralizadas (varias máquinas o equipo), ver telemetría OpenTelemetry en el README del kit.
