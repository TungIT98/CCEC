"""
RAG (Retrieval-Augmented Generation) service for CCEC Climate Platform.

Pure-Python TF-IDF retrieval from the Vietnam Climate Knowledge Base.
No external vector DB required — runs on the markdown KB files on disk.
"""
import math
import os
import re
from pathlib import Path
from typing import Optional

# ── Constants ────────────────────────────────────────────────────────────────────

KB_DIR = Path(os.environ.get("KB_DIR", "E:/ccec-climate-platform/knowledge/climate"))
TOP_K = 4       # top-k chunks to retrieve per query
MAX_CHUNK_WORDS = 120  # max words per chunk
OVERLAP_WORDS = 20     # overlap between chunks


# ── Chunking ────────────────────────────────────────────────────────────────────

def chunk_markdown(text: str, max_words: int = MAX_CHUNK_WORDS, overlap: int = OVERLAP_WORDS):
    """Split markdown text into overlapping word-window chunks."""
    # Split on blank lines first (sections), then on word count
    sections = re.split(r'\n\s*\n', text)
    chunks = []
    for section in sections:
        section = section.strip()
        if not section:
            continue
        words = section.split()
        if len(words) <= max_words:
            chunks.append(section)
        else:
            # Sliding window
            start = 0
            while start < len(words):
                chunk_words = words[start:start + max_words]
                chunks.append(" ".join(chunk_words))
                start += max_words - overlap
    return chunks


def load_kb_chunks(kb_path: Optional[str] = None) -> list[str]:
    """Load and chunk the Vietnam Climate KB markdown file."""
    path = Path(kb_path) if kb_path else KB_DIR / "vietnam-climate-kb.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    return chunk_markdown(text)


# ── TF-IDF Index ────────────────────────────────────────────────────────────────

class SimpleTfidfIndex:
    """In-memory TF-IDF index — no external deps required."""

    def __init__(self, chunks: list[str]):
        self.chunks = chunks
        self.N = len(chunks)
        # Tokenize + normalize
        self._docs = [self._tokenize(c) for c in chunks]
        # Document frequency
        self._df: dict[str, int] = {}
        for doc in self._docs:
            for word in set(doc):
                self._df[word] = self._df.get(word, 0) + 1

    def _tokenize(self, text: str) -> list[str]:
        """Downcase, keep alpha-only words ≥ 2 chars."""
        return [w.lower() for w in re.findall(r"[a-zA-Z]{2,}", text)]

    def _idf(self, word: str) -> float:
        df = self._df.get(word, 0)
        if df == 0:
            return 0.0
        return math.log(self.N / df)

    def score(self, query: str) -> list[tuple[int, float]]:
        """Score all chunks against a query. Returns [(chunk_idx, score), ...] sorted desc."""
        q_terms = self._tokenize(query)
        scores = []
        for idx, doc in enumerate(self._docs):
            score = 0.0
            for term in q_terms:
                tf = doc.count(term)
                if tf == 0:
                    continue
                # TF-IDF: (1 + log tf) * idf
                score += (1 + math.log(tf)) * self._idf(term)
            # Normalize by doc length
            doc_len = len(doc)
            if doc_len > 0:
                score /= math.sqrt(doc_len)
            scores.append((idx, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def retrieve(self, query: str, k: int = TOP_K) -> list[tuple[str, float]]:
        """Return top-k (chunk_text, score) for the query."""
        scored = self.score(query)
        return [(self.chunks[idx], score) for idx, score in scored[:k] if score > 0]


# ── Global index (lazy-loaded) ──────────────────────────────────────────────────

_index: Optional[SimpleTfidfIndex] = None


def get_index() -> SimpleTfidfIndex:
    global _index
    if _index is None:
        chunks = load_kb_chunks()
        if not chunks:
            raise RuntimeError(f"Climate KB not found at {KB_DIR}")
        _index = SimpleTfidfIndex(chunks)
        print(f"[RAG] Indexed {len(chunks)} chunks from Climate KB.")
    return _index


def retrieve_climate_context(query: str, k: int = TOP_K) -> list[str]:
    """Retrieve top-k relevant KB chunks for a user query."""
    try:
        index = get_index()
        results = index.retrieve(query, k=k)
        return [text for text, score in results]
    except Exception as e:
        print(f"[RAG] Retrieval error: {e}")
        return []


def build_rag_context(query: str, k: int = TOP_K) -> str:
    """
    Build a RAG-augmented system context string from the Climate KB.
    Returns a formatted context block to prepend to the system prompt.
    """
    chunks = retrieve_climate_context(query, k=k)
    if not chunks:
        return ""

    context_lines = [
        "## Relevant Climate Knowledge (RAG Retrieved):",
        "",
    ]
    for i, chunk in enumerate(chunks, 1):
        # Strip markdown headers from chunk for cleaner context
        clean = re.sub(r"^#+\s*", "", chunk, flags=re.MULTILINE).strip()
        context_lines.append(f"[Source {i}]:")
        context_lines.append(clean[:500])  # truncate long chunks
        context_lines.append("")
    return "\n".join(context_lines)


# ── System prompt builder ────────────────────────────────────────────────────────

BASE_SYSTEM_PROMPT = (
    "You are a climate expert assistant for the CCEC Climate Platform. "
    "Answer questions about climate change, carbon markets, Vietnam climate policy, "
    "emissions data, and related topics. Be concise, accurate, and helpful. "
    "When referencing data, mention its source and limitations."
)


def build_system_prompt(user_query: str, k: int = TOP_K) -> str:
    """Build full system prompt with RAG context for a given user query."""
    rag_context = build_rag_context(user_query, k=k)
    if rag_context:
        return (
            f"{BASE_SYSTEM_PROMPT}\n\n"
            f"{rag_context}\n\n"
            "Use the retrieved knowledge above to ground your answer. "
            "If the retrieved context does not fully answer the query, say so and "
            "answer based on your general knowledge."
        )
    return BASE_SYSTEM_PROMPT
