---
description: Retoma el proyecto - estado de sync, fase activa, siguiente paso
model: sonnet
---

Retomá el proyecto sin escribir código.

1. Si el brief de inicio no está en el contexto, corré `bash scripts/claude-sync.sh`.
2. Leé `SYNC.md` (pendientes, notas, última línea del log) y la fase activa o siguiente de `ROADMAP.md`.
3. Si el brief dice **MISMATCH**: corré `git log --oneline <head-registrado>..HEAD` y `git diff --stat <head-registrado>` y explicá qué cambió fuera del protocolo.
4. Si hay cambios sin commitear: listalos y preguntá si son de esta fase o restos de otra.
5. Corré `python3 scripts/critical-flows.py check` y mencioná los CF sin test que toca la próxima fase.

Respondé en este formato, corto:
```
Estado: <OK | MISMATCH | sin sync> · rama <x> · <n> cambios sin commitear
Última sesión: <línea del log>
Fase siguiente: <nombre> — <objetivo en una línea>
Toca flujos críticos: <CF-xx o ninguno>
Riesgos: <lo que haya que resolver antes, o "ninguno">
Próximo paso: /fase  (o lo que corresponda)
```
