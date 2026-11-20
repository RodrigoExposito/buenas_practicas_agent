# Arquitectura: {{NOMBRE_PROYECTO}}

## Visión general
{{2-4 líneas: cómo fluye un request de punta a punta}}

## Árbol de archivos
```
{{ARBOL}}
```

| Archivo | Contiene | Fase | Depende de |
|---------|----------|------|------------|
| | | | |

## Modelo de datos
```
{{TABLAS_CAMPOS_RELACIONES}}
```

## Flujos críticos
Fuente de verdad para `scripts/critical-flows.py`. Formato fijo: `| CF-xx | descripción | ruta del test |`.
El test debe contener el ID (ej. `describe("CF-01 ...")`).

| ID | Flujo | Test |
|----|-------|------|
| CF-01 | {{descripción}} | tests/critical/cf-01.test.ts |

## Integraciones externas y MCPs
| Nombre | Para qué flujo | Tools que usamos | Decisión |
|--------|----------------|------------------|----------|
| Playwright MCP | QA de navegador del verificador | navigate, click, screenshot, resize | ADR 0001 |

## Smoke post-deploy
Rutas en `smoke.txt`; se corren con `/postdeploy`.

## Decisiones
Ver `docs/adr/`.
