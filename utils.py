import os
from pathlib import Path

def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

def write_file(filepath: str, content: str):
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
