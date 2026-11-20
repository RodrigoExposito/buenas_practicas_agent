#!/usr/bin/env python3
"""Revisión estática de un componente de terceros (skill, agente, comando, plugin, hook, MCP)
ANTES de instalarlo. No ejecuta nada del componente.

Uso: review-component.py <carpeta-o-archivo>
Clonalo o descomprimilo primero en una carpeta aparte (ej. /tmp/revisar/<nombre>).

Veredicto:
  ROJO      no instalar sin entender cada hallazgo
  AMARILLO  revisar los hallazgos a mano
  VERDE     sin patrones de riesgo conocidos (no garantiza que sea seguro)
"""
import os
import re
import sys

RULES = [
    # (severidad, etiqueta, regex)
    ("ROJO", "descarga y ejecuta (curl|wget ... | sh)", r"(curl|wget)[^\n|]*\|\s*(ba|z)?sh"),
    ("ROJO", "eval / exec dinámico", r"\beval\s*\(|\bexec\s*\(|new Function\("),
    ("ROJO", "decodifica base64 y ejecuta", r"base64\s+(-d|--decode)[^\n]*\|"),
    ("ROJO", "borra en masa", r"rm\s+-rf\s+(/|~|\$HOME|\*)"),
    ("ROJO", "lee credenciales", r"(~|\$HOME)/\.(ssh|aws|config/gh|npmrc|netrc)|id_rsa|\.env\b"),
    ("ROJO", "instrucción de ocultar al usuario", r"(do not|don't|never) (tell|show|mention|inform) (the )?user|no le digas al usuario"),
    ("ROJO", "intenta anular instrucciones", r"ignore (all )?(previous|prior|above) instructions|ignorá las instrucciones"),
    ("ROJO", "desactiva verificaciones", r"--no-verify|--dangerously-skip-permissions|bypassPermissions"),
    ("AMARILLO", "acceso a red", r"\b(curl|wget|fetch\(|axios|requests\.(get|post)|http\.request|nc\s)"),
    ("AMARILLO", "define hooks (se ejecutan solos)", r"\"(PreToolUse|PostToolUse|SessionStart|Stop|UserPromptSubmit|Notification)\""),
    ("AMARILLO", "permisos amplios de tools", r"allowed-tools:\s*(\*|.*\bBash\b(?!\())"),
    ("AMARILLO", "instala paquetes", r"\b(npm|pnpm|yarn)\s+(i|install|add)\b|\bpip3?\s+install\b|\bbrew\s+install\b"),
    ("AMARILLO", "escribe fuera del proyecto", r"(>|>>|tee)\s*(~|\$HOME|/etc|/usr)"),
    ("AMARILLO", "git push / publish", r"git\s+push|npm\s+publish"),
    ("AMARILLO", "blob largo codificado", r"[A-Za-z0-9+/]{200,}={0,2}"),
]
INVISIBLE = re.compile("[\u200b-\u200d\u2060-\u2064\u202a-\u202e\u2066-\u2069\U000e0000-\U000e007f]")
BINARY_EXT = {".exe", ".dll", ".so", ".dylib", ".bin", ".node", ".wasm", ".jar", ".pyc"}


def files_in(target):
    if os.path.isfile(target):
        yield target
        return
    for root, dirs, names in os.walk(target):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules"}]
        for n in names:
            yield os.path.join(root, n)


def main():
    if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
        print(__doc__)
        return 2
    target = sys.argv[1]
    findings = []
    count = 0
    for path in files_in(target):
        count += 1
        rel = os.path.relpath(path, target) if os.path.isdir(target) else os.path.basename(path)
        ext = os.path.splitext(path)[1].lower()
        if ext in BINARY_EXT or (os.access(path, os.X_OK) and ext not in {".sh", ".py", ".js", ".mjs", ".ts"}):
            findings.append(("ROJO", rel, 0, "binario o ejecutable opaco"))
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                lines = fh.readlines()
        except (UnicodeDecodeError, OSError):
            findings.append(("AMARILLO", rel, 0, "archivo no legible como texto"))
            continue
        for i, line in enumerate(lines, 1):
            if INVISIBLE.search(line):
                findings.append(("ROJO", rel, i, "unicode invisible (posible instrucción oculta)"))
            for sev, label, rx in RULES:
                if re.search(rx, line, re.IGNORECASE):
                    findings.append((sev, rel, i, label))

    reds = [f for f in findings if f[0] == "ROJO"]
    yellows = [f for f in findings if f[0] == "AMARILLO"]
    for sev, rel, i, label in reds + yellows:
        print(f"{sev:9} {rel}{':' + str(i) if i else ''}  {label}")
    verdict = "ROJO" if reds else "AMARILLO" if yellows else "VERDE"
    print(f"\n{count} archivos · {len(reds)} rojos · {len(yellows)} amarillos → VEREDICTO: {verdict}")
    if verdict == "VERDE":
        print("Sin patrones conocidos. Igual leé el SKILL.md/agent.md completo antes de instalar.")
    return {"ROJO": 1, "AMARILLO": 0, "VERDE": 0}[verdict]


if __name__ == "__main__":
    sys.exit(main())
