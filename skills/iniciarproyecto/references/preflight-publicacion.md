# Preflight antes de hacer público un repo

Lo usa `/humanizar`. Cada punto se responde con evidencia (comando y salida). Si alguno no es un "sí" claro, frená.

## Secretos y datos
- [ ] Sin claves, tokens ni credenciales en el árbol: `git grep -nEi '(sk-ant-|sk-[a-z0-9]{32,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|BEGIN (RSA |EC )?PRIVATE KEY)'`
- [ ] Tampoco en el historial: `git log -p --all -G '(sk-ant-|AKIA|ghp_)' --oneline | head`
      Si aparece algo: la clave se **rota** igual, aunque después se reescriba el historial.
- [ ] `.env` no está versionado y existe `.env.example` con todas las variables y valores de mentira.
- [ ] Capturas, transcripciones y fixtures revisados: sin datos reales de usuarios, clientes o métricas internas.
- [ ] Sin URLs, hostnames o emails internos.

## Licencias
- [ ] Hay `LICENSE` en la raíz.
- [ ] Dependencias con licencia permisiva (MIT, Apache-2.0, BSD, ISC). Cualquier otra (GPL, AGPL, no comercial, poco clara) queda listada para que el humano decida.
- [ ] Assets (imágenes, fuentes, datasets) propios o con licencia abierta, con atribución si la piden.

## Reproducibilidad
- [ ] Desde un clon limpio, siguiendo solo el README, el proyecto instala y corre.
- [ ] El README dice qué hace, cómo se corre, qué variables necesita y qué limitaciones tiene.
- [ ] Tests y `python3 scripts/critical-flows.py run` en verde.

## Presentación
- [ ] `python3 scripts/ai-lint.py check` limpio.
- [ ] Sin TODOs de plantilla ni `{{placeholders}}` en docs.
- [ ] Mensajes de commit legibles (`python3 scripts/ai-lint.py log`).
