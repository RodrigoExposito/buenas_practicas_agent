---
description: Conventional Commits por grupo lógico, sin push
model: haiku
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git switch:*), Bash(git checkout -b:*), Bash(git branch:*), Bash(git log:*)
---

1. `git status --porcelain` y `git diff --stat`. Si no hay cambios, decilo y terminá.
2. Preguntá: ¿commit en la rama actual (`git branch --show-current`) o en una rama nueva? Si es nueva, proponé nombre `tipo/descripcion-corta`.
3. Agrupá los cambios por **intención** (no por carpeta): una feature, su test y su doc van juntos; un fix aparte; tooling aparte.
4. Mostrá el plan antes de ejecutar:
   ```
   1. feat(invoices): add due date filter   → app/invoices/page.tsx, tests/invoices.test.ts
   2. chore(deps): add date-fns              → package.json, package-lock.json
   ```
5. Por cada grupo: `git add <archivos concretos>` y `git commit -m "<mensaje>"`.
   - Nunca `git add .`, `-A`, `--all` ni `commit -a`.
   - Nunca stagees `.env*`, claves, tokens ni `.claude/settings.local.json`.
   - Mensajes según `docs/WRITING.md`: imperativo, minúscula, sin punto final, sin atribución.
6. Si un hook falla: leé el error, corregí la causa y reintentá. Nunca `--no-verify`.
7. Terminá con `git log --oneline -n <cantidad>` y recordá: **el push lo hacés vos**.
