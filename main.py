"""
Directory Scanner - Scans a directory and outputs all file contents to markdown
with optional token counting, structure-only mode, and tree view mode.
"""

import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import mimetypes
import re

# Optional tiktoken import for accurate GPT token counting
try:
    import tiktoken

    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False


# Directories to skip during scanning
SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
    ".DS_Store",
    "LICENSE",
    "uv.lock",
    ".python-version",
    ".env",
    ".pytest_cache",
}


class TokenCounter:
    """Token counting utilities with multiple methods."""

    def __init__(self):
        self.encoding = None
        if HAS_TIKTOKEN:
            try:
                self.encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
            except Exception:
                pass

    def count_words(self, text: str) -> int:
        return len(text.split())

    def count_characters(self, text: str) -> int:
        return len(text)

    def count_characters_no_spaces(self, text: str) -> int:
        return len(re.sub(r"\s", "", text))

    def estimate_gpt_tokens(self, text: str) -> int:
        return len(text) // 4

    def count_gpt_tokens(self, text: str) -> Optional[int]:
        if self.encoding and text:
            try:
                return len(self.encoding.encode(text))
            except Exception:
                pass
        return None

    def get_all_counts(self, text: str) -> Dict[str, int]:
        counts = {
            "words": self.count_words(text),
            "characters": self.count_characters(text),
            "characters_no_spaces": self.count_characters_no_spaces(text),
            "estimated_gpt_tokens": self.estimate_gpt_tokens(text),
        }
        gpt_tokens = self.count_gpt_tokens(text)
        if gpt_tokens is not None:
            counts["gpt_tokens"] = gpt_tokens
        return counts


def is_text_file(file_path: Path) -> bool:
    try:
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type and mime_type.startswith("text"):
            return True
        text_extensions = {
            ".txt",
            ".md",
            ".py",
            ".js",
            ".html",
            ".css",
            ".json",
            ".xml",
            ".yml",
            ".yaml",
            ".ini",
            ".cfg",
            ".conf",
            ".log",
            ".csv",
            ".sql",
            ".sh",
            ".bat",
            ".ps1",
            ".rb",
            ".go",
            ".java",
            ".cpp",
            ".c",
            ".h",
            ".php",
            ".pl",
            ".r",
            ".scala",
            ".kt",
            ".swift",
            ".ts",
            ".jsx",
            ".tsx",
            ".vue",
            ".svelte",
            ".sass",
            ".scss",
            ".less",
            ".dockerfile",
            ".gitignore",
            ".env",
            ".toml",
            ".lock",
        }
        if file_path.suffix.lower() in text_extensions:
            return True
        with open(file_path, "rb") as f:
            chunk = f.read(1024)
            return b"\x00" not in chunk
    except (OSError, IOError):
        return False


def get_file_extension_for_markdown(file_path: Path) -> str:
    ext_mapping = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".html": "html",
        ".css": "css",
        ".scss": "scss",
        ".sass": "sass",
        ".json": "json",
        ".xml": "xml",
        ".yml": "yaml",
        ".yaml": "yaml",
        ".sql": "sql",
        ".sh": "bash",
        ".bat": "batch",
        ".ps1": "powershell",
        ".rb": "ruby",
        ".go": "go",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".h": "c",
        ".php": "php",
        ".pl": "perl",
        ".r": "r",
        ".scala": "scala",
        ".kt": "kotlin",
        ".swift": "swift",
        ".jsx": "jsx",
        ".tsx": "tsx",
        ".vue": "vue",
        ".dockerfile": "dockerfile",
        ".md": "markdown",
        ".toml": "toml",
    }
    return ext_mapping.get(file_path.suffix.lower(), "text")


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


def main():
    if len(sys.argv) < 2:
        print("Usage: python scanner.py <directory_path> [--path | --path_tree]")
        sys.exit(1)

    structure_only = False
    tree_mode = False
    args = sys.argv[1:]

    if "--path" in args:
        structure_only = True
        args.remove("--path")
    elif "--path_tree" in args:
        tree_mode = True
        args.remove("--path_tree")

    directory_path = Path(args[0])
    if not directory_path.exists():
        print(f"Error: Directory '{directory_path}' does not exist.")
        sys.exit(1)
    if not directory_path.is_dir():
        print(f"Error: '{directory_path}' is not a directory.")
        sys.exit(1)

    token_counter = TokenCounter()
    if not structure_only and not tree_mode:
        if HAS_TIKTOKEN:
            print("✅ Using tiktoken for accurate GPT token counting")
        else:
            print("ℹ️  Using estimated token counting (install tiktoken for accuracy)")

    print(f"Scanning directory: {directory_path.absolute()}")
    files_content = scan_directory(
        directory_path, token_counter, structure_only=structure_only
    )

    output_file = Path(f"{directory_path.name}_scan.md")
    generate_markdown(
        files_content,
        directory_path,
        output_file,
        structure_only=structure_only,
        tree_mode=tree_mode,
    )

    print(f"✅ Scan completed! Output saved to: {output_file.absolute()}")
    print(f"📊 Total files processed: {len(files_content)}")


if __name__ == "__main__":
    main()
