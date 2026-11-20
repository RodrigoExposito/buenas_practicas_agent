---
description: Diagnóstico estructurado cuando algo se rompió o una fase no converge
model: opus
argument-hint: "[síntoma: error, comportamiento, 'la fase C no cierra']"
---

Modo rescate. Síntoma: `$ARGUMENTS`. **No edites nada hasta terminar el diagnóstico y tener aprobación.**

1. **Reproducir.** Conseguí el error exacto (comando + salida). Si no se reproduce, decilo y pedí pasos.
2. **Acotar.** `git log --oneline -15`, `git diff --stat HEAD~5`, `git status`. ¿Desde qué commit falla? Si hace falta, `git stash` (preguntá) y probá en el último commit sano.
3. **Hipótesis.** Máximo 3, ordenadas por probabilidad, cada una con la evidencia a favor y la prueba que la confirma o descarta.
4. **Probar** cada hipótesis con comandos de solo lectura o tests. Mostrá las salidas.
5. **Causa raíz** en una línea, con evidencia.
6. **Plan de arreglo** mínimo: archivos, cambio, test que prueba que quedó arreglado (si es un flujo crítico, el test crítico).
7. **Causa de entorno.** ¿Por qué el sistema dejó pasar esto? (falta un test crítico, regla ausente en AGENTS.md, fase demasiado grande, verificación que se saltó). Proponé el cambio para `docs/HARNESS.md`.

Esperá aprobación. Con el ok: arreglo vía subagente **programador**, verificación vía **verificador**, y `/commit` con `fix(scope): ...`.
Si el problema es que la fase era demasiado grande: proponé partirla con el subagente **arquitecto** en vez de seguir parchando.
