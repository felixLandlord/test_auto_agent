import mimetypes
from pathlib import Path
from .config import TEXT_EXTENSIONS, EXT_MAPPING


def is_text_file(file_path: Path) -> bool:
    try:
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type and mime_type.startswith("text"):
            return True
        
        if file_path.suffix.lower() in TEXT_EXTENSIONS:
            return True
        with open(file_path, "rb") as f:
            chunk = f.read(1024)
            return b"\x00" not in chunk
    except (OSError, IOError):
        return False


def get_file_extension_for_markdown(file_path: Path) -> str:
    return EXT_MAPPING.get(file_path.suffix.lower(), "text")