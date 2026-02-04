from __future__ import annotations

import re
from typing import List


CLAIM_PATTERN = re.compile(r"\b(?:should|must|is|are|will)\b.*?\.", re.IGNORECASE)


def extract_claims(text: str, limit: int = 3) -> List[str]:
    matches = [match.group(0).strip() for match in CLAIM_PATTERN.finditer(text)]
    if matches:
        return matches[:limit]
    sentences = [sentence.strip() for sentence in text.split(".") if sentence.strip()]
    return sentences[:limit]
