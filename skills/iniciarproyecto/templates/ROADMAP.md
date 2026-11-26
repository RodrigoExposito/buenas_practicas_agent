# Roadmap: {{NOMBRE_PROYECTO}}

Reglas: una feature por fase · cada fase termina con un test · sesión nueva por fase (`/clear`) ·
si la fase toca un flujo crítico, su test crítico tiene que existir y pasar.

Aceptación: 3–6 criterios **binarios** por fase. Cada uno se cumple o no, y se comprueba con un comando
o un paso en el navegador. El verificador los marca uno por uno con su evidencia.

Estados: `[ ]` pendiente · `[~]` en curso · `[x]` hecha (con prueba humana)

---

## [ ] Fase A — Setup
**Objetivo:** proyecto corre en local con una página vacía y tests configurados.
**Archivos:** {{lista}}
**Aceptación:**
- [ ] `{{CMD_DEV}}` levanta sin errores en consola
- [ ] `{{CMD_TEST}}` corre (aunque haya 0 tests de producto)
**Flujos críticos:** ninguno
**Prompt para /fase:**
> Implementá la Fase A del ROADMAP.md. Solo esa fase.

---

## [ ] Fase B — {{nombre}}
**Objetivo:**
**Archivos:**
**Aceptación:**
- [ ] {{acción concreta}} → {{resultado observable}}
- [ ] {{caso de error}} → {{mensaje o estado esperado}}
- [ ] {{criterio 3}}
**Flujos críticos:** CF-01 → crear `tests/critical/cf-01.test.ts`
**Prompt para /fase:**
> Implementá la Fase B del ROADMAP.md con TDD. Empezá por el test crítico CF-01.

---

## [ ] Fase Z — Deploy
**Objetivo:** app en producción y smoke en verde.
**Aceptación:**
- [ ] Sin errores en consola · responsive en móvil · formularios validados
- [ ] Variables de entorno cargadas en el proveedor (no en el repo)
- [ ] `/postdeploy` en verde contra la URL de producción
