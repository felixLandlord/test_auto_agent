"""
Directory Scanner - Scans a directory and outputs all file contents to markdown
with optional token counting, structure-only mode, and tree view mode.
"""

import sys
from pathlib import Path
from scanner.token_counter import TokenCounter, HAS_TIKTOKEN
from scanner.core import scan_directory
from scanner.report import generate_markdown


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
