---
description: Review de alta señal del diff - 3 revisores en paralelo y una pasada de validación
argument-hint: "[rango git, ej. main..HEAD; vacío = cambios sin commitear]"
---

Revisá los cambios sin editar nada. Rango pedido: `$ARGUMENTS`.

## 1. Juntar el diff
- Sin argumento: `git diff HEAD` más los archivos nuevos de `git status --porcelain` (los `??` no salen en el diff: leelos enteros).
- Con argumento: `git diff $ARGUMENTS`.
- Si no hay cambios, decilo y terminá.
- Listá las skills `convenciones-*` que aplican a los archivos tocados.

## 2. Revisar (en paralelo)
Lanzá **tres** subagentes **revisor** en un mismo mensaje, uno por foco: `bugs`, `convenciones`, `fallos-silenciosos`.
A cada uno pasale: el foco, el nombre y objetivo de la fase, la lista de archivos tocados y cómo obtener el diff.
No les pases el razonamiento del programador.

## 3. Validar
Por cada hallazgo, lanzá un subagente **revisor** en modo validar (en paralelo) con el hallazgo y su ubicación.
- `CONFIRMADO` → queda.
- `DESCARTADO` → se elimina del informe. No lo menciones como "posible".
Dos revisores que reportan lo mismo cuentan como un solo hallazgo.

## 4. Informe
```
REVIEW: <fase o rango>
VEREDICTO: SIN HALLAZGOS | CON HALLAZGOS

| # | Foco | Ubicación | Problema | Evidencia |
|---|------|-----------|----------|-----------|

Descartados en validación: <n>
```
Si quedó en cero: "Sin hallazgos. Se revisaron bugs, convenciones y fallos silenciosos."

## 5. Qué sigue
- **CON HALLAZGOS** dentro de `/fase`: vuelven al programador. Corrige esos hallazgos y nada más.
- Fuera de `/fase`: mostrá el informe y preguntá si se arreglan ahora o se anotan en `SYNC.md`.

Este review no reemplaza al verificador (que prueba comportamiento) ni a la prueba humana.
