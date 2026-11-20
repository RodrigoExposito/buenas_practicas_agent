#!/usr/bin/env python3
"""Detecta y limpia huellas de texto generado por IA en el repo.

Uso:
  ai-lint.py check [rutas...]   avisos + bloqueos sobre archivos versionados (o las rutas dadas)
  ai-lint.py staged             solo archivos en stage; exit 1 si hay bloqueos (lo usa pre-commit)
  ai-lint.py fix [rutas...]     limpia lo seguro: unicode invisible y espacios raros
  ai-lint.py log                revisa mensajes de commits no pusheados
  ai-lint.py msg <archivo>      borra atribución del mensaje de commit (lo usa commit-msg)

Bloquean: unicode invisible/bidi/TAG, atribución a herramientas.
Avisan: redacción de relleno, comentarios narrativos, código comentado, emojis.
Excepción por línea: comentario "ai-lint: ignore".
"""
import os
import re
import subprocess
import sys

TEXT_EXT = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".json", ".md", ".mdx", ".txt",
    ".css", ".scss", ".html", ".yml", ".yaml", ".toml", ".sh", ".sql", ".go", ".rs",
    ".java", ".kt", ".swift", ".rb", ".php", ".vue", ".svelte", ".env.example",
}
SKIP_DIRS = {"node_modules", ".git", ".next", "dist", "build", "out", "coverage", ".assets-originales"}
# Archivos que citan los patrones a propósito (reglas, detectores)
SELF_SKIP = {os.path.basename(__file__), "review-component.py", "WRITING.md"}

# Bloqueantes
INVISIBLE = re.compile(
    "[\u200b\u200c\u200d\u2060\u2061\u2062\u2063\u2064\u180e"  # zero-width / invisibles
    "\u202a-\u202e\u2066-\u2069"                                # bidi
    "\U000e0000-\U000e007f]"                                     # TAG
)
BOM_INTERNAL = "\ufeff"
ODD_SPACES = re.compile("[\u00a0\u2000-\u200a\u202f\u205f\u3000]")
ATTRIBUTION = re.compile(
    r"(co-authored-by:\s*(claude|anthropic|chatgpt|openai|copilot|cursor|codex|gemini)"
    r"|generated (with|by) (claude|chatgpt|copilot|cursor|an? ai)"
    r"|\U0001f916\s*generated"
    r"|claude\.ai/(code|chat)/[\w-]+)",
    re.IGNORECASE,
)

# Avisos
FILLER = re.compile(
    r"\b(seamless(ly)?|robust|leverag(e|ing)|delve|cutting-edge|state-of-the-art|"
    r"comprehensive solution|it'?s worth noting|in conclusion|sin fisuras|cabe destacar|"
    r"en resumen|de manera eficiente y robusta)\b",
    re.IGNORECASE,
)
NARRATIVE_COMMENT = re.compile(
    r"^\s*(//|#|\*)\s*(this (function|method|component|file|class) (will|is used to|handles)|"
    r"here we|now we|first,? we|step \d+:|esta funci[oó]n (se encarga|va a))",
    re.IGNORECASE,
)
COMMENTED_CODE = re.compile(
    r"^\s*(//|#)\s*(import |from \S+ import|const |let |var |return |console\.log|print\(|"
    r"export |function |def |class )"
)
EMOJI = re.compile("[\U0001f300-\U0001faff\u2600-\u27bf]")
CODE_EXT = TEXT_EXT - {".md", ".mdx", ".txt", ".json"}

BAD_COMMIT_MSG = re.compile(r"^(added|updated|fixed|changed|modified|implemented) ", re.IGNORECASE)
CONVENTIONAL = re.compile(r"^(feat|fix|refactor|test|docs|chore|perf|build|ci|style|revert)(\([\w./-]+\))?!?: .+")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def is_text(path):
    base = os.path.basename(path)
    if base in SELF_SKIP:
        return False
    _, ext = os.path.splitext(base)
    return ext in TEXT_EXT or base in {"Dockerfile", "Makefile", ".gitignore"} or base.endswith(".env.example")


def tracked_files():
    out = run(["git", "ls-files"])
    if out.strip():
        return [f for f in out.splitlines() if os.path.isfile(f)]
    files = []
    for root, dirs, names in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        files += [os.path.join(root, n)[2:] for n in names]
    return files


def staged_files():
    out = run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"])
    return [f for f in out.splitlines() if os.path.isfile(f)]


def scan_file(path):
    blocks, warns = [], []
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().split("\n")
    except (UnicodeDecodeError, OSError):
        return blocks, warns
    _, ext = os.path.splitext(path)
    is_code = ext in CODE_EXT
    for i, line in enumerate(lines, 1):
        if "ai-lint: ignore" in line:
            continue
        loc = f"{path}:{i}"
        if INVISIBLE.search(line):
            blocks.append(f"{loc}  unicode invisible/bidi")
        if BOM_INTERNAL in line and not (i == 1 and line.startswith(BOM_INTERNAL)):
            blocks.append(f"{loc}  BOM interno")
        if ATTRIBUTION.search(line):
            blocks.append(f"{loc}  atribución a herramienta IA")
        if ODD_SPACES.search(line):
            warns.append(f"{loc}  espacio no estándar (fix lo corrige)")
        if FILLER.search(line):
            warns.append(f"{loc}  relleno: '{FILLER.search(line).group(0)}'")
        if is_code and NARRATIVE_COMMENT.search(line):
            warns.append(f"{loc}  comentario narrativo")
        if is_code and COMMENTED_CODE.search(line):
            warns.append(f"{loc}  código comentado")
        if is_code and EMOJI.search(line):
            warns.append(f"{loc}  emoji en código")
    return blocks, warns


def report(files, strict):
    all_b, all_w = [], []
    for f in files:
        if is_text(f):
            b, w = scan_file(f)
            all_b += b
            all_w += w
    for b in all_b:
        print(f"BLOQUEA  {b}")
    for w in all_w:
        print(f"aviso    {w}")
    print(f"\nai-lint: {len(all_b)} bloqueos, {len(all_w)} avisos en {len(files)} archivos.")
    if all_b:
        print("Corregí los bloqueos (o 'ai-lint.py fix' para unicode/espacios).")
    return 1 if (strict and all_b) else 0


def fix(files):
    changed = 0
    for f in files:
        if not is_text(f):
            continue
        try:
            with open(f, encoding="utf-8") as fh:
                src = fh.read()
        except (UnicodeDecodeError, OSError):
            continue
        out = INVISIBLE.sub("", src)
        head, rest = (out[:1], out[1:]) if out.startswith(BOM_INTERNAL) else ("", out)
        out = head + rest.replace(BOM_INTERNAL, "")
        out = ODD_SPACES.sub(" ", out)
        if out != src:
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(out)
            changed += 1
            print(f"limpiado  {f}")
    print(f"ai-lint fix: {changed} archivos modificados. Atribución y redacción: revisar a mano o con /humanizar.")
    return 0


def clean_message(path):
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    kept = [l for l in lines if not ATTRIBUTION.search(l)]
    text = INVISIBLE.sub("", "\n".join(kept)).rstrip() + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    subject = next((l for l in text.split("\n") if l.strip() and not l.startswith("#")), "")
    if subject and not CONVENTIONAL.match(subject) and not subject.startswith(("Merge ", "Revert ")):
        print(f"aviso commit-msg: '{subject}' no sigue Conventional Commits (ver docs/WRITING.md)")
    return 0


def check_log():
    upstream = run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"]).strip()
    rng = f"{upstream}..HEAD" if upstream else "HEAD"
    out = run(["git", "log", rng, "--format=%h%x09%B%x1e"])
    issues = 0
    for entry in filter(None, (e.strip() for e in out.split("\x1e"))):
        sha, _, body = entry.partition("\t")
        subject = body.split("\n", 1)[0]
        problems = []
        if ATTRIBUTION.search(body):
            problems.append("atribución")
        if not CONVENTIONAL.match(subject) and not subject.startswith(("Merge ", "Revert ")):
            problems.append("no conventional")
        if BAD_COMMIT_MSG.match(subject):
            problems.append("pasado/genérico")
        if EMOJI.search(subject):
            problems.append("emoji")
        if problems:
            issues += 1
            print(f"{sha}  {subject}  -> {', '.join(problems)}")
    scope = "no pusheados" if upstream else "sin upstream (revisé toda la historia local)"
    print(f"\nai-lint log: {issues} commits con observaciones ({scope}).")
    return 0


def main():
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help"}:
        print(__doc__)
        return 0
    mode, args = sys.argv[1], sys.argv[2:]
    if mode == "check":
        return report(args or tracked_files(), strict=False)
    if mode == "staged":
        return report(staged_files(), strict=True)
    if mode == "fix":
        return fix(args or tracked_files())
    if mode == "log":
        return check_log()
    if mode == "msg" and args:
        return clean_message(args[0])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
