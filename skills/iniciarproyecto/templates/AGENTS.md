# {{NOMBRE_PROYECTO}}

> Contexto canónico para cualquier agente (Claude Code, Codex, Cursor). Mantenerlo en 50–100 líneas.
> Regla de oro: si borrar una línea hace que el agente se equivoque, queda. Si no, se va.

## Producto
{{DEFINICION_UN_PARRAFO}}
Detalle: `docs/PRODUCT.md`. Arquitectura: `docs/ARCHITECTURE.md`. Plan: `ROADMAP.md`.

## Stack
- Framework: {{FRAMEWORK}}
- Estilos: {{ESTILOS}}
- Datos: {{DB}}
- Auth: {{AUTH_O_NINGUNA}}
- Deploy: {{DEPLOY}}
- Paquetes: npm

## Comandos
- Dev: `{{CMD_DEV}}`
- Tests: `{{CMD_TEST}}`
- Tests críticos: `{{CMD_TEST_CRITICOS}}`
- Lint/types: `{{CMD_LINT}}`
- Build: `{{CMD_BUILD}}`

## Estructura
{{REGLAS_DE_CARPETAS}}
<!-- ej: páginas en /app, componentes en /components, acceso a datos solo en /lib/db.ts, APIs en /app/api -->

## Estilo de código
- TypeScript estricto, sin `any` salvo justificación en comentario.
- Funciones y componentes chicos; archivos < 200 líneas.
- async/await; errores manejados explícitamente, nunca tragados.
- Nombres descriptivos en inglés. Comentarios solo para el "por qué", no el "qué".
- Convenciones detalladas: skills en `.claude/skills/convenciones-*`.

## Flujos críticos
Listados en `docs/ARCHITECTURE.md` (CF-xx). Todo cambio que los toque necesita su test crítico en verde.
Nunca borres ni debilites un test crítico para que pase.

## Reglas de trabajo
- Una fase del `ROADMAP.md` por sesión. No adelantes trabajo de otras fases.
- Antes de decir "listo": correr tests y mostrar la salida. Sin evidencia, no está listo.
- Si no pudiste verificar algo (sin red, sin permisos, comando que falla), decilo como **BLOQUEO** con la causa. No inventes que funcionó ni busques un atajo silencioso.
- No agregues dependencias sin justificarlas en el resumen de la fase.
- No hagas `git push`, `git add .`, `--no-verify` ni `reset --hard`.
- No leas ni escribas `.env*`. Variables nuevas: documentalas en `.env.example`.
- Escritura de docs, comentarios y commits: `docs/WRITING.md`.

## Estado
Fase activa y pendientes: `SYNC.md` (el brief de inicio de sesión lo resume).
