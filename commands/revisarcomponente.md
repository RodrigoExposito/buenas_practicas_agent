---
description: Revisa una skill, agente, comando, plugin o MCP de terceros antes de instalarlo
argument-hint: "<carpeta local, archivo o URL de repo>"
model: sonnet
---

Componente: `$ARGUMENTS`. **No instales ni ejecutes nada del componente durante la revisión.**

1. Si es una URL de repo: pedí permiso y cloná en una carpeta aislada (`git clone --depth 1 <url> /tmp/revisar/<nombre>`). Si es un comando tipo `npx ... install`, no lo corras: buscá el repo fuente.
2. Escaneo estático:
   `python3 ~/.claude/skills/iniciarproyecto/scripts/review-component.py <carpeta>`
3. Lectura completa de los archivos que se cargan en contexto o se ejecutan: `SKILL.md`, `*.md` de agentes/comandos, `hooks`, scripts, `.mcp.json`/manifest.
   Respondé estas preguntas con evidencia (archivo:línea):
   - ¿Qué instrucciones le da al modelo? ¿Alguna pide ocultar algo, anular reglas o actuar sin preguntar?
   - ¿Qué se ejecuta solo (hooks) y cuándo?
   - ¿Qué tools/permisos pide? ¿Son proporcionales a lo que promete?
   - ¿Toca red, credenciales, archivos fuera del proyecto?
   - Si es MCP: ¿cuántas tools expone y cuántas usarías? (muchas sin usar = contexto desperdiciado)
   - ¿Choca con el kit? (ej. otro `/commit`, hooks que hacen push, permisos que pisan los `deny`)
4. Veredicto: **INSTALAR | INSTALAR CON CAMBIOS | NO INSTALAR**, con los cambios concretos si aplica (ej. borrar un hook, restringir `allowed-tools`).
5. Si se instala, anotá en `docs/HARNESS.md`: fecha, componente, versión/commit revisado, veredicto.
