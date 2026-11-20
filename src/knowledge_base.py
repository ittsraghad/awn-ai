from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "docs" / "knowledge_base.md"

DEFAULT_CHUNK_SIZE = 900


def load_knowledge_base() -> str:
    """Load the knowledge base Markdown document."""

    if not KNOWLEDGE_BASE_PATH.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {KNOWLEDGE_BASE_PATH}"
        )

    content = KNOWLEDGE_BASE_PATH.read_text(encoding="utf-8")

    if not content.strip():
        raise ValueError("Knowledge base is empty.")

    return content


def split_long_text(text: str, max_chars: int) -> list[str]:
    """Split long text into smaller pieces without losing its content."""

    if len(text) <= max_chars:
        return [text]

    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        if len(sentence) > max_chars:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            for start in range(0, len(sentence), max_chars):
                chunks.append(sentence[start:start + max_chars].strip())

            continue

        candidate = f"{current_chunk} {sentence}".strip()

        if len(candidate) <= max_chars:
            current_chunk = candidate
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())

            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def split_knowledge_base(
    content: str,
    max_chars: int = DEFAULT_CHUNK_SIZE
) -> list[dict]:
    """
    Split the knowledge base into searchable chunks.
    Each chunk keeps its parent section and subsection.
    """

    chunks = []

    current_section = None
    current_subsection = None
    current_content = []

    def save_current_content():

        if not current_content or not current_section:
            return

        text = "\n".join(current_content).strip()

        if not text:
            return

        text_parts = split_long_text(text, max_chars)

        for part in text_parts:

            chunks.append({
                "chunk_id": f"chunk_{len(chunks) + 1:03d}",
                "title": current_subsection or current_section,
                "section": current_section,
                "subsection": current_subsection,
                "content": part
            })

    for line in content.splitlines():

        if line.startswith("## "):

            save_current_content()

            current_section = line[3:].strip()
            current_subsection = None
            current_content = []

            if current_section.startswith("Version"):
                current_section = None

        elif line.startswith("### ") and current_section:

            save_current_content()

            current_subsection = line[4:].strip()
            current_content = []

        elif current_section:
            current_content.append(line)

    save_current_content()

    return chunks


def get_knowledge_documents() -> list[dict]:
    """Load the knowledge base and return searchable chunks."""

    content = load_knowledge_base()

    return split_knowledge_base(content)