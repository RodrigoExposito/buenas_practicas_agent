# Guía de escritura (código, docs, commits)

El objetivo: que el repo se lea como escrito por un equipo cuidadoso, no como salida de un modelo.

## Comentarios
- Explican el **por qué** o una restricción no obvia. Nunca narran lo que el código ya dice.
- Mal: `// This function will fetch the user data`  ·  Bien: `// Cache 60s: el proveedor limita a 10 req/min`
- Nada de código comentado (`// import React`), ni `TODO` sin dueño o fase (`TODO(fase-D): ...`).
- Sin emojis en código, logs ni commits.

## Docs
- Frases cortas, voz activa, presente. Primero el dato, después el contexto.
- Prohibido el relleno: "robusto", "potente", "sin fisuras", "cabe destacar", "en resumen", "seamless", "leverage", "delve".
- Listas solo si el contenido es una lista. Nada de títulos para párrafos de dos líneas.

## Commits (Conventional Commits)
- `tipo(scope): descripción` en imperativo y minúscula: `feat(invoices): add due date filter`.
- Tipos: feat, fix, refactor, test, docs, chore, perf, build, ci.
- Cuerpo opcional: el por qué, no la lista de archivos.
- Mal: `Added new feature for invoices`, `Updated files`, `fix stuff`.
- Sin `Co-Authored-By` de herramientas ni "Generated with". El hook `commit-msg` lo borra igual.

## Nombres
- Variables y funciones por lo que representan (`overdueInvoices`), no por su tipo (`dataArray`).
- Sin prefijos genéricos: `handleData`, `processStuff`, `utils2`.

## Excepción puntual
Si una línea necesita romper una regla del linter: comentario `ai-lint: ignore` en esa línea, con motivo.
