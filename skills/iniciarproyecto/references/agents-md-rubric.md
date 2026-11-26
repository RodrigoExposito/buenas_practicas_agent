# Rúbrica de AGENTS.md / CLAUDE.md

La usa `/cerrarsesion` para decidir qué agregar, qué corregir y qué borrar.
Principio: el archivo viaja en cada request. Cada línea tiene que ganarse el lugar.

## Puntaje (100)

| Criterio | Puntos | Se cumple cuando |
|----------|--------|------------------|
| Comandos | 20 | dev, tests, tests críticos, lint/types y build están y funcionan tal como figuran |
| Mapa de arquitectura | 20 | carpetas clave, puntos de entrada y dónde vive el acceso a datos |
| Gotchas | 15 | lo no obvio está escrito: workarounds, orden de inicialización, quirks de config |
| Concisión | 15 | sin relleno ni cosas que el código ya dice; 50–100 líneas |
| Vigencia | 15 | comandos, rutas y stack coinciden con el repo de hoy |
| Accionabilidad | 15 | instrucciones concretas, comandos copiables, rutas reales |

Nota: 90+ A · 75+ B · 60+ C · menos de 60, reescribir.

## Cómo auditar
1. Leé el archivo entero.
2. Contrastalo con el repo: ¿existen las rutas que nombra? ¿los comandos están en `package.json` o equivalente?
3. Puntuá cada criterio y listá los problemas concretos con su línea.
4. Proponé el cambio como diff. No apliques sin aprobación.

## Qué SÍ agregar
- Comandos descubiertos en la sesión que no estaban.
- Gotchas que costaron tiempo ("los tests corren en serie por la DB compartida").
- Dependencias entre módulos que no se ven en el código.
- Quirks de configuración o de entorno.

## Qué NO agregar
- Lo que se deduce leyendo el código ("`UserService` maneja usuarios").
- Buenas prácticas genéricas que valen para cualquier proyecto.
- Arreglos puntuales que no se van a repetir.
- Detalle de un dominio: eso va en la skill `convenciones-*`, que se carga solo cuando aplica.
- Estado de la fase: eso vive en `SYNC.md`.

## Señales de alarma
- Comandos que fallarían (ruta mal, dependencia que ya no está).
- Referencias a archivos o carpetas borrados.
- Texto de plantilla sin completar (`{{...}}`).
- La misma regla escrita en dos archivos.
- Una regla que se violó dos veces: no alcanza con dejarla escrita, hay que convertirla en hook.
