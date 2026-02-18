import re
from typing import Dict, Optional

# Optional tiktoken import for accurate GPT token counting
try:
    import tiktoken

    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False


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