---
description: Limpia huella IA en comentarios, docs y commits no pusheados (sin tocar lógica) y corre el preflight de publicación
argument-hint: "[rutas opcionales]"
---

Objetivo: que el repo se lea escrito por un equipo cuidadoso. Reglas en `docs/WRITING.md`.

1. `python3 scripts/ai-lint.py fix $ARGUMENTS` (unicode invisible y espacios raros, automático).
2. `python3 scripts/ai-lint.py check $ARGUMENTS` y agrupá los avisos por archivo.
3. Por archivo, reescribí **solo**:
   - comentarios narrativos → borrar o convertir en el "por qué",
   - código comentado → borrar,
   - relleno en docs → frase directa,
   - emojis en código/logs → fuera.
   **Prohibido** cambiar lógica, nombres públicos, firmas o tests. Si un cambio de texto afecta comportamiento (strings de UI, mensajes de error que se testean), no lo toques y listalo.
4. Commits: `python3 scripts/ai-lint.py log`. Si hay commits **no pusheados** con mensajes malos, proponé los nuevos mensajes y pedí aprobación. Con ok, reescribí con `git rebase -i` (el humano confirma el comando). Nunca toques commits ya pusheados.
5. Corré tests para confirmar que no cambió nada funcional y mostrá el resumen: archivos tocados, avisos antes/después.
6. **Si el repo se va a publicar o mostrar**, recorré `~/.claude/skills/iniciarproyecto/references/preflight-publicacion.md` punto por punto, con el comando y su salida como evidencia. Lo que no sea un "sí" claro se lista como pendiente para el humano. Si aparece una clave en el historial, avisá que hay que rotarla aunque se reescriba el historial; no reescribas historial ya pusheado.
