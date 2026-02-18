from pathlib import Path
from typing import List, Tuple, Dict
from .token_counter import TokenCounter
from .config import SKIP_DIRS
from .utils import is_text_file


def scan_directory(
    directory_path: Path, token_counter: TokenCounter, structure_only=False
) -> List[Tuple[Path, str, Dict[str, int]]]:
    files_content = []
    for file_path in directory_path.rglob("*"):
        if any(skip in file_path.parts for skip in SKIP_DIRS):
            continue
        if file_path.is_file():
            if structure_only:
                files_content.append((file_path, "", {}))
            else:
                try:
                    if is_text_file(file_path):
                        with open(
                            file_path, "r", encoding="utf-8", errors="ignore"
                        ) as f:
                            content = f.read()
                        token_counts = token_counter.get_all_counts(content)
                        files_content.append((file_path, content, token_counts))
                    else:
                        token_counts = {
                            "words": 0,
                            "characters": 0,
                            "characters_no_spaces": 0,
                            "estimated_gpt_tokens": 0,
                        }
                        files_content.append((file_path, "[Binary file]", token_counts))
                except (OSError, IOError, UnicodeDecodeError) as e:
                    error_msg = f"[Error reading file: {e}]"
                    token_counts = token_counter.get_all_counts(error_msg)
                    files_content.append((file_path, error_msg, token_counts))
    return files_content


def generate_tree(directory_path: Path) -> str:
    """Generate a tree-like structure of the directory."""
    tree_lines = []

    def walk(dir_path: Path, prefix=""):
        entries = sorted(
            [e for e in dir_path.iterdir() if e.name not in SKIP_DIRS],
            key=lambda x: (x.is_file(), x.name.lower()),
        )
        for i, entry in enumerate(entries):
            connector = "└── " if i == len(entries) - 1 else "├── "
            tree_lines.append(f"{prefix}{connector}{entry.name}")
            if entry.is_dir():
                extension = "    " if i == len(entries) - 1 else "│   "
                walk(entry, prefix + extension)

    tree_lines.append(directory_path.name)
    walk(directory_path)
    return "\n".join(tree_lines)