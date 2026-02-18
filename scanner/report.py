from pathlib import Path
from typing import List, Tuple, Dict
from .core import generate_tree
from .utils import get_file_extension_for_markdown


def generate_markdown(
    files_content: List[Tuple[Path, str, Dict[str, int]]],
    base_path: Path,
    output_file: Path,
    structure_only=False,
    tree_mode=False,
) -> None:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# Directory Scan: {base_path.name}\n\n")
        f.write(f"**Scanned Path:** `{base_path.absolute()}`\n\n")
        f.write(f"**Total Files:** {len(files_content)}\n\n")
        f.write("---\n\n")

        if tree_mode:
            f.write("## 📂 Project Structure\n\n")
            f.write("```text\n")
            f.write(generate_tree(base_path))
            f.write("\n```\n")
            return

        for file_path, content, counts in sorted(files_content):
            try:
                relative_path = file_path.relative_to(base_path)
            except ValueError:
                relative_path = file_path
            f.write(f"## 📄 {relative_path}\n\n")
            f.write(f"**Full Path:** `{file_path.absolute()}`\n\n")
            if not structure_only:
                if content == "[Binary file]":
                    f.write("*This is a binary file and cannot be displayed.*\n\n")
                elif content.startswith("[Error reading file:"):
                    f.write(f"*{content}*\n\n")
                elif not content.strip():
                    f.write("*This file is empty.*\n\n")
                else:
                    language = get_file_extension_for_markdown(file_path)
                    f.write(f"```{language}\n{content}\n```\n\n")
            f.write("---\n\n")