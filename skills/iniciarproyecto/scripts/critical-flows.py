#!/usr/bin/env python3
"""Gate de flujos críticos. Fuente de verdad: tabla "Flujos críticos" en docs/ARCHITECTURE.md.

Uso:
  critical-flows.py check [--strict]   estado de cada CF (strict: exit 1 si falta alguno)
  critical-flows.py summary            una línea para el brief de sesión
  critical-flows.py run                corre el comando "Tests críticos" de AGENTS.md (exit = el del comando)

Un CF está "ok" si su archivo de test existe y menciona su ID (ej. describe("CF-01 ...")).
"""
import os
import re
import shlex
import subprocess
import sys

ARCH = "docs/ARCHITECTURE.md"
AGENTS = "AGENTS.md"
ROW = re.compile(r"^\|\s*(CF-\d+)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")


def flows():
    if not os.path.isfile(ARCH):
        return None
    out = []
    with open(ARCH, encoding="utf-8") as fh:
        for line in fh:
            m = ROW.match(line)
            if m:
                out.append(m.groups())
    return out


def status(cf, path):
    path = path.strip("` ")
    if not path or not os.path.isfile(path):
        return "pendiente", "sin archivo de test"
    with open(path, encoding="utf-8", errors="ignore") as fh:
        if cf not in fh.read():
            return "sin-id", f"{path} no menciona {cf}"
    return "ok", path


def check(strict):
    items = flows()
    if items is None:
        print(f"critical-flows: no existe {ARCH}")
        return 1 if strict else 0
    if not items:
        print("critical-flows: la tabla no tiene CF definidos")
        return 1 if strict else 0
    bad = 0
    for cf, desc, path in items:
        st, detail = status(cf, path)
        bad += st != "ok"
        print(f"{st:10} {cf}  {desc}  ({detail})")
    print(f"\n{len(items) - bad}/{len(items)} flujos críticos con test.")
    return 1 if (strict and bad) else 0


def summary():
    items = flows()
    if not items:
        return 0
    states = [status(cf, p)[0] for cf, _, p in items]
    missing = [cf for (cf, _, _), st in zip(items, states) if st != "ok"]
    line = f"flujos críticos: {states.count('ok')}/{len(items)} con test"
    if missing:
        line += f" · faltan: {', '.join(missing)}"
    print(line)
    return 0


def run():
    cmd = None
    if os.path.isfile(AGENTS):
        with open(AGENTS, encoding="utf-8") as fh:
            for line in fh:
                m = re.search(r"Tests cr[ií]ticos:\s*`([^`]+)`", line)
                if m and "{{" not in m.group(1):
                    cmd = m.group(1)
    if not cmd:
        print("critical-flows: definí '- Tests críticos: `comando`' en AGENTS.md")
        return 2
    print(f"$ {cmd}")
    return subprocess.call(shlex.split(cmd))


def main():
    args = sys.argv[1:]
    mode = args[0] if args else "check"
    if mode == "check":
        return check("--strict" in args)
    if mode == "summary":
        return summary()
    if mode == "run":
        return run()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
