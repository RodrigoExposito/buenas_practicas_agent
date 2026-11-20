---
name: iniciarproyecto
description: Arranca un proyecto nuevo (o hace retrofit de uno existente) con plan, estructura, roles de modelo, controles, observabilidad y protocolo de sync. Usar cuando el usuario escribe /iniciarproyecto o pide iniciar/estructurar un proyecto.
model: opus
---

# /iniciarproyecto

Convertís una idea vaga en un proyecto listo para que agentes trabajen de forma limpia y controlada.
Principio rector: **los agentes hacen el trabajo; el humano especifica, observa y controla.**

Reglas de ejecución:
- Corrés las etapas en orden. **STOP al final de cada etapa**: mostrás el resultado y esperás "ok" o correcciones.
- Nunca escribís código de producto en esta skill. Solo docs, configuración y scaffolding vacío.
- Toda plantilla vive en `~/.claude/skills/iniciarproyecto/templates/`; todo script en `.../scripts/`. Copialos, no los reescribas de memoria.
- Si algo no lo pudiste verificar (comando que falló, sin red, archivo ausente), lo decís explícitamente. Nunca reportes una etapa como lista sin evidencia.
- Idioma: el del usuario. Commits y código en inglés salvo que el usuario pida otra cosa.

Argumento: `$ARGUMENTS` = descripción de la idea (puede venir vacío).

---

## Etapa 0 — Recon

1. `git rev-parse --is-inside-work-tree` y `git log --oneline -5`. Si no hay repo: pedí `git init` (no lo hagas sin permiso).
2. Detectá modo:
   - **Nuevo**: repo vacío o solo README.
   - **Retrofit**: ya hay código. Leé `package.json`/`pyproject.toml`, estructura de carpetas y README. No toques `src/`.
3. En retrofit corré el diagnóstico: `python3 ~/.claude/skills/iniciarproyecto/scripts/ai-lint.py check` (avisos de huella IA) y listá qué docs del kit faltan.
4. Mostrá: modo, stack detectado, qué falta. **STOP.**

## Etapa 1 — Idea

Si `$ARGUMENTS` no alcanza, preguntá (máximo 5 preguntas, en una sola tanda):
- Qué hace, explicado a un amigo.
- Para quién, específico.
- La ÚNICA acción principal del usuario.
- Inspiración ("como X pero para Y").
- Dónde vive (web, móvil, extensión, CLI, no sé).

Devolvé una definición de un párrafo:
`[Nombre] es una [tipo] que ayuda a [usuario] a [acción principal] mediante [cómo]. A diferencia de [alternativa], [diferenciador].`
**STOP.**

## Etapa 2 — Alcance → `docs/PRODUCT.md`

Usá `templates/PRODUCT.md`. Chequeo de realidad, en voz alta:
- ¿Entra en 5–15 archivos de producto? Si no, recortá.
- ¿Cada feature sirve a la acción principal? Si no, va al Parking Lot V2.
- ¿Puede salir sin login? Entonces V1 sin auth.
- ¿Alcanza SQLite/JSON/Supabase? Empezá por lo más simple.

Máximo 5–7 features V1. Nivel de complejidad (simple / moderado / complejo / recortar).
**Flujos críticos**: identificá 1–4 flujos que si se rompen el producto no sirve (ej. "crear factura", "login", "checkout"). Van a tener test obligatorio. Asignales IDs `CF-01`, `CF-02`…
**STOP.**

## Etapa 3 — Stack → `docs/adr/0001-stack.md`

El stack más simple que no se rompa:
- Web sin backend → HTML + Tailwind + JS. Deploy: Netlify/Vercel.
- Con datos → Next.js + SQLite (o Supabase si hay multiusuario/auth).
- Dashboard/herramienta interna → Next.js + shadcn/ui + SQLite.
- Extensión Chrome → Manifest V3 + JS.
- Con IA → Next.js + API de Anthropic.
- No sabés → Next.js + Tailwind + SQLite.

Decidí también:
- Comando de tests y de tests de flujos críticos.
- **MCPs del proyecto** (lista blanca, ver `templates/mcp.json`). Por defecto solo Playwright para QA de navegador. Cada MCP extra necesita justificación de una línea: qué flujo lo usa y cuántas tools expone. Si un MCP genérico trae decenas de tools para usar dos, anotá "evaluar MCP propio mínimo" en el Parking Lot.

Escribí el ADR con `templates/ADR.md` (contexto, opciones, decisión, consecuencias). **STOP.**

## Etapa 4 — Arquitectura → `docs/ARCHITECTURE.md`

Con `templates/ARCHITECTURE.md`:
- Árbol de archivos completo antes de escribir código. Por archivo: qué contiene, en qué fase nace, de qué depende.
- Modelo de datos (tablas/campos/relaciones).
- Tabla de **Flujos críticos**: `| CF-01 | descripción | tests/critical/cf-01.test.ts |`. El archivo de test todavía no existe; lo crea la fase que implementa el flujo.
- **Rutas de smoke** para post-deploy (`smoke.txt`): ruta + status esperado.
**STOP.**

## Etapa 5 — Plan → `ROADMAP.md`

Con `templates/ROADMAP.md`. Fases pequeñas: una feature por fase, cada una con:
- Objetivo, archivos que toca, criterios de aceptación verificables.
- Test que la cierra (y si toca un CF, el test crítico correspondiente).
- Prompt listo para `/fase`.
Orden típico: Setup → Layout → Feature principal → Datos → Features secundarias → Pulido → Deploy.
**STOP.**

## Etapa 6 — Scaffolding

Copiá y completá (preguntá antes de sobrescribir cualquier archivo existente):

| Origen (templates/) | Destino |
|---|---|
| `AGENTS.md` | `AGENTS.md` (contexto canónico, portable a Codex/Cursor) |
| `CLAUDE.md` | `CLAUDE.md` (importa `@AGENTS.md` + reglas propias de Claude) |
| `SYNC.md` | `SYNC.md` |
| `WRITING.md` | `docs/WRITING.md` |
| `HARNESS.md` | `docs/HARNESS.md` (log de lecciones del entorno) |
| `settings.json` | `.claude/settings.json` |
| `mcp.json` | `.mcp.json` (solo los MCPs aprobados en Etapa 3) |
| `gitignore` | `.gitignore` (merge si existe) |
| `githooks/*` | `.githooks/` + `git config core.hooksPath .githooks` |
| `smoke.txt` | `smoke.txt` con las rutas de la Etapa 4 |
| `project-skill.md` | `.claude/skills/convenciones-<dominio>/SKILL.md` |

Scripts: copiá todo `scripts/` a `scripts/` del proyecto y `chmod +x scripts/*.sh scripts/*.py .githooks/*`.

**Skills de proyecto**: generá 1–2 skills de convenciones (ej. `convenciones-api`, `convenciones-ui`) con el patrón exacto que el código debe seguir (estructura de un endpoint, manejo de errores, naming). CLAUDE.md queda corto porque viaja en cada request; el detalle va en skills que se cargan solo cuando aplican.

Creá las carpetas vacías del árbol de la Etapa 4 con `.gitkeep`. Sin código de producto.

Verificá y mostrá evidencia:
- `bash scripts/claude-sync.sh` produce el brief.
- `python3 scripts/ai-lint.py check` sale limpio.
- `python3 scripts/critical-flows.py check` lista los CF como "pendiente" (normal hasta que existan los tests).
**STOP.**

## Etapa 7 — Commits baseline

Commits por grupo lógico, sin push:
1. `docs: add product spec, architecture and roadmap`
2. `chore: add agent context, settings and project skills`
3. `chore: add sync, lint and verification scripts`
4. `chore: add git hooks and gitignore`

Después: `bash scripts/claude-sync-update.sh --commit`.

Cerrá con el paso a paso para el usuario:
```
/clear  →  /retomar  →  /fase  →  /cerrarsesion  →  git push (vos)
```
Y recordá: reiniciar Claude Code para que tome `.claude/settings.json` y `.mcp.json`.

---

## Retrofit (repo existente)

Mismas etapas, pero:
- Etapa 1–2 se infieren del código y README; confirmás con el usuario.
- Etapa 4 documenta la arquitectura **real**, no la ideal. Las deudas van a `ROADMAP.md` como fases de refactor.
- Flujos críticos: identificá los existentes y marcá cuáles no tienen test. Ese hueco es la primera fase del roadmap.
- Nunca modificás `src/` en esta skill.
