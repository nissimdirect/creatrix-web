#!/usr/bin/env python3
"""Build script: injects card data from creatrix source files into index.html."""
import json
import sys
from pathlib import Path

CREATRIX_DIR = Path.home() / "Development" / "creatrix"
WEB_DIR = Path.home() / "Development" / "creatrix-web"

def load_originals():
    cards = []
    with open(CREATRIX_DIR / "oblique-strategies.txt") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                cards.append(line)
    return cards

def load_mutants():
    tagged = []
    current = None
    with open(CREATRIX_DIR / "mutant-strategies.txt") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# ---") and line.endswith("---"):
                current = line.replace("# ---", "").replace("---", "").strip()
            elif line and not line.startswith("#"):
                tagged.append({"card": line, "tradition": current or "Unknown"})
    return tagged

def load_directives():
    sys.path.insert(0, str(CREATRIX_DIR))
    from directives import DIRECTIVES
    return list(DIRECTIVES)

def build():
    originals = load_originals()
    mutants = load_mutants()
    directives = load_directives()

    print(f"Originals: {len(originals)}")
    print(f"Mutants:   {len(mutants)}")
    print(f"Directives: {len(directives)}")
    print(f"Total deck: {len(originals) + len(mutants)}")

    template = (WEB_DIR / "index.html").read_text()

    template = template.replace(
        "ORIGINALS_PLACEHOLDER",
        json.dumps(originals, ensure_ascii=False)
    )
    template = template.replace(
        "MUTANTS_PLACEHOLDER",
        json.dumps(mutants, ensure_ascii=False)
    )
    template = template.replace(
        "DIRECTIVES_PLACEHOLDER",
        json.dumps(directives, ensure_ascii=False)
    )

    (WEB_DIR / "index.html").write_text(template)
    print("Built index.html with embedded card data")

if __name__ == "__main__":
    build()
