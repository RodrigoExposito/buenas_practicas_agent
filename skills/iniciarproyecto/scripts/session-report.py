#!/usr/bin/env python3
"""Observabilidad de sesiones de Claude Code sin infraestructura extra.

Lee las transcripciones locales (~/.claude/projects/<proyecto>/*.jsonl) y reporta:
tokens y caché, pico de contexto, tools más usadas, resultados más pesados, uso de MCPs
y recomendaciones concretas para abaratar el entorno.

Uso:
  session-report.py                 última sesión de este repo
  session-report.py --last 5        agrega las últimas 5 sesiones
  session-report.py --file X.jsonl  una transcripción puntual
Escribe además .claude/reports/session-<fecha>.md
"""
import argparse
import collections
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys

CONTEXT_WINDOW = int(os.environ.get("CONTEXT_WINDOW", "200000"))


def repo_root():
    try:
        return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return os.getcwd()


def transcript_dir(root):
    base = os.path.expanduser("~/.claude/projects")
    guess = os.path.join(base, re.sub(r"[^A-Za-z0-9]", "-", root))
    if os.path.isdir(guess):
        return guess
    for d in glob.glob(os.path.join(base, "*")):  # fallback: buscar por cwd dentro del jsonl
        for f in sorted(glob.glob(os.path.join(d, "*.jsonl")), key=os.path.getmtime)[-1:]:
            try:
                with open(f, encoding="utf-8") as fh:
                    for line in fh:
                        if json.loads(line).get("cwd") == root:
                            return d
            except Exception:
                continue
    return None


def text_len(content):
    if isinstance(content, str):
        return len(content)
    if isinstance(content, list):
        return sum(text_len(c.get("text", c.get("content", ""))) if isinstance(c, dict) else len(str(c))
                   for c in content)
    return len(str(content or ""))


def analyze(files):
    usage = collections.Counter()
    tools = collections.Counter()
    result_chars = collections.Counter()
    heavy = []
    reads = collections.Counter()
    id_to_tool = {}
    peak = 0
    turns = 0
    sidechain_calls = 0
    for path in files:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                try:
                    e = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = e.get("message") or {}
                if e.get("type") == "assistant":
                    u = msg.get("usage") or {}
                    for k in ("input_tokens", "output_tokens", "cache_read_input_tokens",
                              "cache_creation_input_tokens"):
                        usage[k] += u.get(k, 0) or 0
                    ctx = sum((u.get(k, 0) or 0) for k in ("input_tokens", "cache_read_input_tokens",
                                                           "cache_creation_input_tokens"))
                    if not e.get("isSidechain"):
                        peak = max(peak, ctx)
                    for c in msg.get("content") or []:
                        if isinstance(c, dict) and c.get("type") == "tool_use":
                            name = c.get("name", "?")
                            tools[name] += 1
                            id_to_tool[c.get("id")] = name
                            if e.get("isSidechain"):
                                sidechain_calls += 1
                            if name == "Read":
                                reads[(c.get("input") or {}).get("file_path", "?")] += 1
                elif e.get("type") == "user":
                    content = msg.get("content")
                    if isinstance(content, str):
                        turns += 1
                        continue
                    for c in content or []:
                        if isinstance(c, dict) and c.get("type") == "tool_result":
                            name = id_to_tool.get(c.get("tool_use_id"), "?")
                            n = text_len(c.get("content"))
                            result_chars[name] += n
                            heavy.append((n, name))
                        elif isinstance(c, dict) and c.get("type") == "text":
                            turns += 1
    return dict(usage=usage, tools=tools, result_chars=result_chars, heavy=sorted(heavy, reverse=True)[:5],
                reads=reads, peak=peak, turns=turns, sidechain=sidechain_calls)


def configured_mcps(root):
    p = os.path.join(root, ".mcp.json")
    try:
        with open(p, encoding="utf-8") as fh:
            return list((json.load(fh).get("mcpServers") or {}).keys())
    except Exception:
        return []


def fmt(n):
    return f"{n:,}".replace(",", ".")


def render(data, root, files):
    u = data["usage"]
    cache_read = u["cache_read_input_tokens"]
    fresh = u["input_tokens"] + u["cache_creation_input_tokens"]
    hit = cache_read / (cache_read + fresh) if (cache_read + fresh) else 0
    peak_pct = data["peak"] / CONTEXT_WINDOW if CONTEXT_WINDOW else 0
    total_res = sum(data["result_chars"].values()) or 1

    mcp_use = collections.Counter()
    for name, n in data["tools"].items():
        if name.startswith("mcp__"):
            mcp_use[name.split("__")[1]] += n

    out = [f"# Reporte de sesión — {os.path.basename(root)}",
           f"{len(files)} transcripción(es) · {dt.datetime.now():%Y-%m-%d %H:%M}", "",
           "## Tokens",
           f"- Input nuevo: {fmt(u['input_tokens'])} · escritura en caché: {fmt(u['cache_creation_input_tokens'])}",
           f"- Leído de caché: {fmt(cache_read)} · output: {fmt(u['output_tokens'])}",
           f"- Aprovechamiento de caché: {hit:.0%}",
           f"- Pico de contexto (hilo principal): {fmt(data['peak'])} ({peak_pct:.0%} de {fmt(CONTEXT_WINDOW)})",
           f"- Turnos humanos: {data['turns']} · tool calls en subagentes: {data['sidechain']}", "",
           "## Tools más usadas"]
    for name, n in data["tools"].most_common(8):
        share = data["result_chars"][name] / total_res
        out.append(f"- {name}: {n} llamadas · {share:.0%} del volumen de resultados")
    out += ["", "## Resultados más pesados (~tokens)"]
    for n, name in data["heavy"]:
        out.append(f"- {name}: ~{fmt(n // 4)}")
    out += ["", "## MCPs"]
    configured = configured_mcps(root)
    for s in sorted(set(configured) | set(mcp_use)):
        out.append(f"- {s}: {mcp_use.get(s, 0)} llamadas{' (configurado)' if s in configured else ' (no está en .mcp.json)'}")
    if not configured and not mcp_use:
        out.append("- ninguno")

    rec = []
    if peak_pct > 0.6:
        rec.append("Pico de contexto > 60%: partir la fase en sub-fases o delegar exploración a subagentes.")
    if (cache_read + fresh) and hit < 0.5:
        rec.append("Caché < 50%: evitá cambiar CLAUDE.md/skills a mitad de sesión y reiniciar seguido; eso invalida el prefijo cacheado.")
    for name, n in data["result_chars"].most_common(1):
        if n / total_res > 0.4:
            rec.append(f"'{name}' genera {n / total_res:.0%} del volumen: pedí salidas más acotadas (head/grep, rangos de líneas) o filtralo con un script.")
    for s in configured:
        if mcp_use.get(s, 0) == 0:
            rec.append(f"MCP '{s}' configurado y sin uso: si no lo usa ninguna fase, sacalo de .mcp.json (sus tools ocupan contexto igual).")
    for s, n in mcp_use.items():
        distinct = {t for t in data["tools"] if t.startswith(f"mcp__{s}__")}
        if len(distinct) <= 2 and n >= 5:
            rec.append(f"MCP '{s}': usás solo {len(distinct)} tool(s). Evaluá un MCP propio mínimo o un script.")
    rereads = [f for f, n in data["reads"].items() if n >= 3]
    auto = {"AGENTS.md", "CLAUDE.md"}
    ctx_files = [os.path.basename(f) for f in rereads if os.path.basename(f) in auto]
    other = [os.path.basename(f) for f in rereads if os.path.basename(f) not in auto]
    if other:
        rec.append(f"Archivos leídos 3+ veces: {', '.join(other[:4])}. Si es contexto estable, resumilo en AGENTS.md o en una skill.")
    if ctx_files:
        rec.append(f"{', '.join(ctx_files)} se releyó 3+ veces aunque ya entra solo al contexto: agregá en CLAUDE.md 'no releer AGENTS.md salvo cambios'.")
    out += ["", "## Recomendaciones"] + ([f"- {r}" for r in rec] or ["- Sin alertas. El entorno está liviano."])
    out += ["", "_Llevar las que apliquen a docs/HARNESS.md vía /cerrarsesion._"]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--last", type=int, default=1)
    ap.add_argument("--file")
    a = ap.parse_args()
    root = repo_root()
    if a.file:
        files = [a.file]
    else:
        d = transcript_dir(root)
        if not d:
            print("BLOQUEO: no encontré transcripciones de este repo en ~/.claude/projects. "
                  "¿Corriste Claude Code desde esta carpeta en esta máquina?")
            return 2
        files = sorted(glob.glob(os.path.join(d, "*.jsonl")), key=os.path.getmtime)[-a.last:]
        if not files:
            print(f"BLOQUEO: {d} no tiene transcripciones.")
            return 2
    report = render(analyze(files), root, files)
    print(report)
    os.makedirs(os.path.join(root, ".claude", "reports"), exist_ok=True)
    path = os.path.join(root, ".claude", "reports", f"session-{dt.datetime.now():%Y%m%d-%H%M}.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(report)
    print(f"(guardado en {os.path.relpath(path, root)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
