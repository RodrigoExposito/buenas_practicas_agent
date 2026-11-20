# Kit /iniciarproyecto · v2

Un comando para arrancar (o hacer retrofit de) un proyecto con plan, estructura, roles de modelo,
controles, observabilidad y protocolo de sync.

Principio: **los agentes hacen el trabajo; vos especificás, observás y controlás.**

| Pilar | Qué lo implementa |
|-------|-------------------|
| Especificar | `PRODUCT.md`, `ARCHITECTURE.md`, `ROADMAP.md`, ADRs, `AGENTS.md`, skills `convenciones-*` |
| Observar | `/auditarsesion` (transcripciones locales), telemetría OTel opcional, `docs/HARNESS.md` |
| Controlar | `permissions` deny/ask, hooks de git, lista blanca de MCPs, gate de flujos críticos, prueba humana, push manual |

---

## 1. Instalación (una vez, en tu Mac)

```bash
git clone https://github.com/RodrigoExposito/buenas_practicas_agent.git && cd buenas_practicas_agent
./install.sh --dry-run     # muestra qué va a crear o reemplazar
./install.sh               # instala en ~/.claude (backup .bak-<fecha> de lo que difiera)
```

1. Reiniciá Claude Code.
2. Corré `/agents` → tienen que aparecer **arquitecto**, **programador**, **verificador**.
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
| 1 Idea | definición en un párrafo | ¿es esto? |
| 2 Alcance | `docs/PRODUCT.md` + **flujos críticos (CF-xx)** | qué entra en V1 |
| 3 Stack | `docs/adr/0001-stack.md` + **MCPs permitidos** | stack y MCPs |
| 4 Arquitectura | `docs/ARCHITECTURE.md` + tabla de CF + rutas de smoke | árbol y datos |
| 5 Plan | `ROADMAP.md` (una feature por fase) | orden de fases |
| 6 Scaffolding | AGENTS.md, CLAUDE.md, settings, `.mcp.json`, hooks, scripts, skills de convenciones | revisás archivos |
| 7 Baseline | 4 commits, sin push | `git push` |

Al terminar: **reiniciá Claude Code** para que tome `.claude/settings.json` y `.mcp.json`
(la primera vez te pide aprobar el MCP de Playwright).

## 3. Ciclo por fase (una sesión por fase)

```
/clear
/retomar          → estado, fase siguiente, CF que toca, riesgos
/fase             → programador (TDD) → verificador (tests + navegador desktop/móvil)
                    → gate de flujos críticos → TU prueba manual → /commit
/cerrarsesion     → log, lecciones del entorno, SYNC.md commiteado, qué re-subir al Project
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
| Antes de publicar o mostrar el repo | `/humanizar` |
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
│   ├── templates/
│   │   ├── AGENTS.md            contexto canónico, portable (Codex/Cursor lo leen)
│   │   ├── CLAUDE.md            importa @AGENTS.md + reglas propias de Claude
│   │   ├── PRODUCT.md  ARCHITECTURE.md  ROADMAP.md  ADR.md  SYNC.md
│   │   ├── WRITING.md           guía de escritura
│   │   ├── HARNESS.md           log de lecciones del entorno
│   │   ├── project-skill.md     plantilla de skill convenciones-<dominio>
│   │   ├── settings.json        permisos allow/ask/deny + hook SessionStart + MCPs habilitados
│   │   ├── settings.telemetry.json   OTel opcional (va a settings.local.json)
│   │   ├── mcp.json             lista blanca: solo Playwright por defecto
│   │   ├── smoke.txt  gitignore
│   │   └── githooks/            pre-commit (secretos, unicode, atribución) · commit-msg
│   └── scripts/
│       ├── claude-sync.sh  claude-sync-update.sh  sync-manifest.txt
│       ├── critical-flows.py    gate de flujos críticos (check / summary / run)
│       ├── smoke-test.sh        smoke HTTP post-deploy
│       ├── session-report.py    observabilidad desde transcripciones locales
│       ├── review-component.py  escaneo estático de componentes de terceros
│       ├── ai-lint.py           huellas IA en texto
│       └── clean-assets.sh      metadata IA en imágenes/video (exiftool/ffmpeg)
├── agents/   arquitecto (opus) · programador (sonnet) · verificador (sonnet, QA en navegador)
└── commands/ retomar · fase · commit (haiku) · cerrarsesion · rescate (opus) · humanizar
              auditarsesion · postdeploy · revisarcomponente
```

## Qué cambió respecto de v1

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

## Ajustes típicos

- Otro stack por defecto: Etapa 3 de `SKILL.md` y bloque Stack de `templates/AGENTS.md`.
- IDs exactos de modelo en los agents: `model: claude-opus-5-5` / `claude-sonnet-5-5`.
- Más MCPs por defecto: agregalos en `templates/mcp.json` **y** en `enabledMcpjsonServers` de `templates/settings.json`.
- Cursor/Windsurf: leen `AGENTS.md`; si tu versión no, copiá su contenido a `.cursorrules` / `.windsurfrules`.

## Licencia

MIT. Ver `LICENSE`.
