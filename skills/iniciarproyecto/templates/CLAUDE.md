@AGENTS.md

# Específico de Claude Code

## Roles de modelo
- `arquitecto` (Opus): plan, datos, ADRs. No toca código de producto.
- `programador` (Sonnet): implementa UNA fase con TDD.
- `verificador` (Sonnet): QA ciego. No edita. Tests + navegador + flujos críticos.
- `revisor` (Sonnet): lee el diff con un foco (bugs, convenciones, fallos silenciosos). No edita.

## Comandos del kit
- `/retomar` dónde estamos · `/fase` implementar la siguiente fase · `/commit` commits por grupo lógico
- `/revisar` review de alta señal del diff (lo llama `/fase`; también sirve suelto)
- `/cerrarsesion` log + lecciones del entorno · `/rescate` cuando algo se rompió
- `/auditarsesion` dónde se fue el contexto y qué abaratar · `/postdeploy` smoke en producción
- `/revisarcomponente <ruta>` antes de instalar una skill/agente/plugin de terceros
- `/humanizar` limpiar huella IA en comentarios, docs y commits no pusheados

## Contexto
- Brief automático al iniciar sesión (hook `SessionStart` → `scripts/claude-sync.sh`).
- Si el contexto pasa ~60%, terminá la unidad de trabajo y sugerí `/cerrarsesion` + `/clear`. No hagas `/compact` en medio de una fase.
- Exploración amplia (buscar en muchos archivos) → subagente, para no ensuciar el hilo principal.

## Hooks
- `PostToolUse` sobre Edit/Write → `scripts/post-edit.sh`: formatea y chequea el archivo editado. Si devuelve errores, se corrigen antes de seguir.

## MCPs
Solo los de `.mcp.json`. No sugieras instalar MCPs nuevos sin pasar por el ADR de stack.
