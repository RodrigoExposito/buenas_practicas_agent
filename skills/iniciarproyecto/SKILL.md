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

Entrevista corta e iterativa. No mandes un cuestionario.

1. **Abrí con una sola pregunta abierta**: "Contame qué querés construir, como se lo explicarías a un amigo."
   Si `$ARGUMENTS` ya lo cuenta, salteá este paso.
2. **Dejá que explique antes de sugerir.** Una repregunta abierta ("¿qué haría exactamente? ¿cómo se ve una buena primera versión?") antes de reencuadrar, recortar o proponer opciones.
3. **Después, tandas de 2–3 preguntas**, solo las que su respuesta dejó abiertas. Cuando las respuestas posibles se pueden enumerar, ofrecé opciones (AskUserQuestion) en vez de pedir texto libre. Como máximo una pregunta abierta por turno. Tenés que salir sabiendo:
   - para quién es, específico;
   - la ÚNICA acción principal del usuario;
   - inspiración ("como X pero para Y");
   - dónde vive (web, móvil, extensión, CLI, no sé).
4. **Límites en contexto.** Si la idea choca con algo real (necesita una credencial, una API paga, tiempo real), decilo en el momento en que aparece, con el camino alternativo. No abras con una lista de advertencias.

Reglas de redacción:
- El problema se escribe con las palabras del usuario (cita o paráfrasis cercana). No inventes cifras, tamaños de equipo ni dolores que no dijo.
- No prometas duraciones que no podés sostener.

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
**Parking Lot**: todo lo que queda fuera de V1 se anota en el momento, con versión (V2, V3), el motivo y cómo se haría. El motivo es uno de tres, sin mezclarlos: `no es posible` · `falta credencial o acceso` · `fuera de alcance de V1`. "Todavía no" siempre va con "y así se hace después".
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

Antes de decidir, presentá **2–3 enfoques** con sus trade-offs: el mínimo (menos piezas, más reuso), el más limpio (más mantenible, más trabajo inicial) y uno intermedio. Una tabla corta, tu recomendación con el motivo, y el usuario elige. Si de verdad hay una sola opción razonable, decilo en una línea en vez de inventar alternativas. Lo descartado queda en la sección "Opciones" del ADR.

Decidí también:
- Comando de tests y de tests de flujos críticos.
- Formateador, linter y chequeo de tipos del stack (ej. prettier + eslint + tsc, o ruff). Los usa el hook de edición `scripts/post-edit.sh`.
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
- Objetivo y archivos que toca.
- **3–6 criterios de aceptación binarios**: se cumplen o no, y cada uno se puede comprobar con un comando o un paso en el navegador. "Funciona bien" no es un criterio; "al enviar el formulario vacío aparece el error 'Campo requerido'" sí.
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
| `github/claude-review.yml` | `.github/workflows/claude-review.yml` (**opcional**, ver abajo) |

Scripts: copiá todo `scripts/` a `scripts/` del proyecto y `chmod +x scripts/*.sh scripts/*.py .githooks/*`.

**Skills de proyecto**: generá 1–2 skills de convenciones (ej. `convenciones-api`, `convenciones-ui`) con el patrón exacto que el código debe seguir (estructura de un endpoint, manejo de errores, naming). CLAUDE.md queda corto porque viaja en cada request; el detalle va en skills que se cargan solo cuando aplican.

**Hook de edición**: `templates/settings.json` registra `scripts/post-edit.sh` como `PostToolUse` sobre Edit/Write. Formatea y chequea el archivo recién editado con las herramientas que el proyecto tenga instaladas, y le devuelve al agente los errores que queden. Si el stack no es JS/TS ni Python, adaptá el script al formateador y linter elegidos en la Etapa 3, o avisá que el hook no va a hacer nada.

**Review en CI (opcional)**: preguntá si quiere review automática de PRs en GitHub. Explicá el costo antes de copiar nada: necesita el secret `ANTHROPIC_API_KEY` en el repo y cada review consume tokens de esa clave. Con el ok, copiá el workflow. El merge y el push siguen siendo del humano.

Creá las carpetas vacías del árbol de la Etapa 4 con `.gitkeep`. Sin código de producto.

Verificá y mostrá evidencia:
- `bash scripts/claude-sync.sh` produce el brief.
- `python3 scripts/ai-lint.py check` sale limpio.
- `python3 scripts/critical-flows.py check` lista los CF como "pendiente" (normal hasta que existan los tests).
- `echo '{"tool_input":{"file_path":"README.md"}}' | bash scripts/post-edit.sh; echo $?` devuelve 0.
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
`/fase` encadena: programador → verificador → `/revisar` → gate de flujos críticos → prueba humana → `/commit`.
Y recordá: reiniciar Claude Code para que tome `.claude/settings.json` y `.mcp.json`.

---

## Retrofit (repo existente)

Mismas etapas, pero:
- Etapa 1–2 se infieren del código y README; confirmás con el usuario.
- Si el repo es grande, explorá con 2–3 subagentes en paralelo, cada uno con un ángulo (flujo principal de punta a punta, acceso a datos, tests y build). Cada uno devuelve los 5–10 archivos clave; después leelos vos antes de documentar.
- Etapa 4 documenta la arquitectura **real**, no la ideal. Las deudas van a `ROADMAP.md` como fases de refactor.
- Flujos críticos: identificá los existentes y marcá cuáles no tienen test. Ese hueco es la primera fase del roadmap.
- Nunca modificás `src/` en esta skill.
