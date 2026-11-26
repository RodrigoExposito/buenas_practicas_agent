# Kit /iniciarproyecto · v3

Un comando para arrancar (o hacer retrofit de) un proyecto con plan, estructura, roles de modelo,
controles, observabilidad y protocolo de sync.

Principio: **los agentes hacen el trabajo; vos especificás, observás y controlás.**

| Pilar | Qué lo implementa |
|-------|-------------------|
| Especificar | `PRODUCT.md`, `ARCHITECTURE.md`, `ROADMAP.md`, ADRs, `AGENTS.md`, skills `convenciones-*` |
| Observar | `/auditarsesion` (transcripciones locales), telemetría OTel opcional, `docs/HARNESS.md` |
| Controlar | `permissions` deny/ask, hooks de git, hook de edición (formato, lint, tipos), review del diff con `/revisar`, lista blanca de MCPs, gate de flujos críticos, prueba humana, push manual |

---

## 1. Instalación (una vez, en tu Mac)

```bash
git clone https://github.com/RodrigoExposito/buenas_practicas_agent.git && cd buenas_practicas_agent
./install.sh --dry-run     # muestra qué va a crear o reemplazar
./install.sh               # instala en ~/.claude (backup .bak-<fecha> de lo que difiera)
```

1. Reiniciá Claude Code.
2. Corré `/agents` → tienen que aparecer **arquitecto**, **programador**, **verificador**, **revisor**.
3. Opcional para limpiar assets: `brew install exiftool ffmpeg`.

Requisitos: git, python3, node/npx (para el MCP de Playwright).

## 2. Proyecto nuevo

```bash
mkdir mi-app && cd mi-app && git init && claude
```
```
/iniciarproyecto app para que freelancers trackeen facturas
```

Recorre 8 etapas y **para al final de cada una** para que apruebes:

| Etapa | Qué sale | Tu decisión |
|-------|----------|-------------|
| 0 Recon | modo nuevo/retrofit | — |
| 1 Idea | entrevista corta por tandas → definición en un párrafo | ¿es esto? |
| 2 Alcance | `docs/PRODUCT.md` + **flujos críticos (CF-xx)** + Parking Lot con motivo y versión | qué entra en V1 |
| 3 Stack | 2–3 enfoques con trade-offs → `docs/adr/0001-stack.md` + **MCPs permitidos** | enfoque, stack y MCPs |
| 4 Arquitectura | `docs/ARCHITECTURE.md` + tabla de CF + rutas de smoke | árbol y datos |
| 5 Plan | `ROADMAP.md` (una feature por fase, 3–6 criterios binarios) | orden de fases |
| 6 Scaffolding | AGENTS.md, CLAUDE.md, settings, `.mcp.json`, hooks, scripts, skills de convenciones, workflow de review en CI (opcional) | revisás archivos; CI sí o no |
| 7 Baseline | 4 commits, sin push | `git push` |

Al terminar: **reiniciá Claude Code** para que tome `.claude/settings.json` y `.mcp.json`
(la primera vez te pide aprobar el MCP de Playwright).

## 3. Ciclo por fase (una sesión por fase)

```
/clear
/retomar          → estado, fase siguiente, CF que toca, riesgos
/fase             → programador (TDD) → verificador (tests + navegador desktop/móvil)
                    → /revisar (3 revisores + validación) → gate de flujos críticos
                    → TU prueba manual → /commit
/cerrarsesion     → log, lecciones del entorno, vigencia de AGENTS.md, SYNC.md commiteado, qué re-subir
git push          → vos
```

Qué hacés vos en cada fase:
1. Leer el resumen de `/retomar` (10 segundos).
2. Si el programador o el verificador reportan **BLOQUEO**, resolverlo (dar acceso, datos, levantar un servicio).
3. Probar a mano el checklist que te muestra `/fase` y confirmar.
4. Aprobar o rechazar los cambios de entorno que propone `/cerrarsesion`.
5. `git push`.

## 4. Deploy

```
/postdeploy https://mi-app.vercel.app
```
Smoke HTTP de `smoke.txt` + recorrido de flujos críticos en producción (solo lectura, desktop y móvil).
Veredicto: SANO / DEGRADADO / CAÍDO. Si no está sano → `/rescate`.

## 5. Mantenimiento del entorno

| Cuándo | Comando |
|--------|---------|
| Una sesión se sintió lenta, cara o confusa | `/auditarsesion` (o `--last 5`) |
| Algo se rompió o una fase no converge en 2 vueltas | `/rescate <síntoma>` |
| Antes de instalar una skill/agente/plugin/MCP ajeno | `/revisarcomponente <carpeta o repo>` |
| Querés una segunda lectura de un diff fuera de `/fase` | `/revisar` (o `/revisar main..HEAD`) |
| Antes de publicar o mostrar el repo | `/humanizar` (incluye el preflight de publicación) |
| Imágenes/video generados con IA | `bash scripts/clean-assets.sh public` |

## 6. Repo existente (retrofit)

Dentro del repo: `/iniciarproyecto`. Documenta la arquitectura **real**, identifica flujos críticos sin test
(esa es la primera fase del roadmap), instala hooks/settings/scripts y muestra el diagnóstico de `ai-lint`.
No toca código de producto.

---

## Qué instala

```
~/.claude/
├── skills/iniciarproyecto/
│   ├── SKILL.md                 pipeline de 8 etapas (Opus)
│   ├── references/
│   │   ├── agents-md-rubric.md  rúbrica para auditar AGENTS.md / CLAUDE.md
│   │   └── preflight-publicacion.md   checklist antes de hacer público un repo
│   ├── templates/
│   │   ├── AGENTS.md            contexto canónico, portable (Codex/Cursor lo leen)
│   │   ├── CLAUDE.md            importa @AGENTS.md + reglas propias de Claude
│   │   ├── PRODUCT.md  ARCHITECTURE.md  ROADMAP.md  ADR.md  SYNC.md
│   │   ├── WRITING.md           guía de escritura
│   │   ├── HARNESS.md           log de lecciones del entorno
│   │   ├── project-skill.md     plantilla de skill convenciones-<dominio>
│   │   ├── settings.json        permisos allow/ask/deny + hooks SessionStart y PostToolUse + MCPs habilitados
│   │   ├── settings.telemetry.json   OTel opcional (va a settings.local.json)
│   │   ├── mcp.json             lista blanca: solo Playwright por defecto
│   │   ├── smoke.txt  gitignore
│   │   ├── github/claude-review.yml   review de PRs en CI (opcional)
│   │   └── githooks/            pre-commit (secretos, unicode, atribución) · commit-msg
│   └── scripts/
│       ├── claude-sync.sh  claude-sync-update.sh  sync-manifest.txt
│       ├── critical-flows.py    gate de flujos críticos (check / summary / run)
│       ├── post-edit.sh         hook de edición: formato, lint y tipos del archivo tocado
│       ├── smoke-test.sh        smoke HTTP post-deploy
│       ├── session-report.py    observabilidad desde transcripciones locales
│       ├── review-component.py  escaneo estático de componentes de terceros
│       ├── ai-lint.py           huellas IA en texto
│       └── clean-assets.sh      metadata IA en imágenes/video (exiftool/ffmpeg)
├── agents/   arquitecto (opus) · programador (sonnet) · verificador (sonnet, QA en navegador)
│             revisor (opus, lee el diff con un foco)
└── commands/ retomar · fase · commit (haiku) · cerrarsesion · rescate (opus) · humanizar
              auditarsesion · postdeploy · revisarcomponente · revisar
```

## Qué cambió en v3

Ideas tomadas de los repos públicos de Anthropic (`claude-plugins-official`, `launch-your-agent`,
`claude-code-action`, `skills`, `claude-code-playground`) y adaptadas al flujo del kit.

| # | Cambio | Dónde |
|---|--------|-------|
| 1 | **Review del diff de alta señal**: tres revisores en paralelo (bugs, convenciones, fallos silenciosos) y una pasada que valida cada hallazgo | agente `revisor`, `/revisar`, paso 4 de `/fase` |
| 2 | **Criterios de aceptación binarios** (3–6 por fase) y tabla criterio / veredicto / evidencia | `ROADMAP.md`, arquitecto, verificador |
| 3 | **Hook de edición**: formato, lint y tipos sobre cada archivo tocado; regla violada dos veces → control determinista | `post-edit.sh`, `settings.json`, `/cerrarsesion` |
| 4 | **Entrevista iterativa**: una pregunta abierta, después tandas cortas con opciones | Etapa 1 |
| 5 | **Parking Lot con versión, motivo y cómo** | `PRODUCT.md`, Etapa 2 |
| 6 | **2–3 enfoques con trade-offs** antes de fijar el stack; exploración en paralelo en retrofit | Etapa 3, arquitecto |
| 7 | **Auditoría de vigencia de AGENTS.md / CLAUDE.md** con rúbrica | `/cerrarsesion`, `references/agents-md-rubric.md` |
| 8 | **Review de PRs en CI** (opcional) con permisos mínimos | `templates/github/claude-review.yml`, Etapa 6 |
| 9 | **Preflight de publicación** y pautas para escribir skills cortas | `/humanizar`, `references/preflight-publicacion.md`, `project-skill.md` |

Notas:
- El hook de edición solo corre herramientas que el proyecto ya tiene instaladas (prettier, eslint, tsc, ruff).
  Sin ninguna, no hace nada. `POST_EDIT_TSC=0` saltea el chequeo de tipos si tsc es lento en tu proyecto.
  Usa `.venv/bin/ruff` si existe, porque los hooks heredan el PATH del shell y no el del entorno virtual.
- El `revisor` usa Opus: cada `/revisar` lanza tres revisores y una validación por hallazgo. Si el costo pesa, cambiá `model:` a `sonnet` en `agents/revisor.md`.
- El workflow de CI necesita el secret `ANTHROPIC_API_KEY` y consume tokens en cada PR. No pushea ni mergea.
- Proyectos creados con v2: copiá `scripts/post-edit.sh` y agregá el bloque `PostToolUse` de `templates/settings.json`
  a mano; los agentes y comandos se actualizan solos al reinstalar.

## Qué cambió en v2 (respecto de v1)

| # | Cambio | Dónde |
|---|--------|-------|
| 1 | **Nunca OK sin evidencia**: todo lo no verificado se declara BLOQUEO / NO VERIFICADO | AGENTS.md, programador, verificador |
| 2 | **QA en navegador** desktop + móvil (390×844) con capturas, consola y red | verificador + Playwright MCP |
| 3 | **Flujos críticos** con test obligatorio; la fase no cierra si fallan | PRODUCT, ARCHITECTURE, `critical-flows.py`, `/fase` |
| 4 | **Smoke post-deploy** | `smoke.txt`, `smoke-test.sh`, `/postdeploy` |
| 5 | **MCPs mínimos**: lista blanca y justificación por MCP | `mcp.json`, `enabledMcpjsonServers`, Etapa 3 |
| 6 | **Skills de convenciones** por proyecto; CLAUDE.md corto | `project-skill.md`, Etapa 6 |
| 7 | **Observabilidad** de sesiones y OTel opcional | `session-report.py`, `/auditarsesion` |
| 8 | **Iterar el entorno**: cada fricción → cambio de regla/skill/hook aprobado | `/cerrarsesion`, `HARNESS.md` |
| 9 | **Revisión de componentes de terceros** | `review-component.py`, `/revisarcomponente` |
| 10 | **AGENTS.md** como fuente canónica | AGENTS.md + CLAUDE.md con `@AGENTS.md` |

Además: permisos `ask` para instalar dependencias, deploy y `curl`; detección de claves en el diff;
`clean-assets.sh` usa exiftool/ffmpeg (ya no requiere `--with-assets` ni uv).

**Decisión deliberada:** el kit mantiene la prueba humana en cada fase y el push manual.
La review la hacen agentes, pero el merge y el push los decide una persona.

## Telemetría OpenTelemetry (opcional)

`/auditarsesion` funciona sin nada extra. Si querés métricas centralizadas (varias máquinas, costos por proyecto),
mergeá `templates/settings.telemetry.json` en `.claude/settings.local.json` del proyecto y levantá un colector OTel
en el endpoint configurado. Verificá los nombres de variables contra la documentación vigente de Claude Code.

## Plugins recomendados (aparte, no forman parte del kit)

De better-claude (midudev, comunidad, no afiliado a Anthropic). **Pasalos por `/revisarcomponente` antes de instalar.**

| Plugin | Para qué |
|--------|----------|
| Sub Meter | uso de la suscripción en la barra de estado |
| Token Meter | tokens por turno; señal para `/clear` |
| `use-haiku` / `think-hard` | prefijos `_` (Haiku) y `+` (esfuerzo máximo) |
| `/after` | cola de prompts |

No instales el `/commit` de better-claude junto con el del kit.

Del directorio oficial de Anthropic (`anthropics/claude-plugins-official`). También pasan por `/revisarcomponente`.

| Plugin | Para qué | A tener en cuenta |
|--------|----------|-------------------|
| `security-guidance` | avisos por patrón al editar, revisión del diff al terminar el turno y revisión al commitear | las revisiones con modelo consumen tokens de tu cuenta; trae hooks propios que corren en `git commit` |

`/plugin install security-guidance@claude-plugins-official`

## Ajustes típicos

- Otro stack por defecto: Etapa 3 de `SKILL.md` y bloque Stack de `templates/AGENTS.md`.
- IDs exactos de modelo en los agents: `model: claude-opus-5-5` / `claude-sonnet-5-5`.
- Más MCPs por defecto: agregalos en `templates/mcp.json` **y** en `enabledMcpjsonServers` de `templates/settings.json`.
- Cursor/Windsurf: leen `AGENTS.md`; si tu versión no, copiá su contenido a `.cursorrules` / `.windsurfrules`.

## Licencia

MIT. Ver `LICENSE`.
