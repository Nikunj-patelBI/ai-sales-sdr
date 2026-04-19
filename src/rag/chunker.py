"""Chunking strategies by content type."""
from __future__ import annotations


def chunk_company_profile(company: dict) -> str:
    """Company profile: one chunk per company. Serialize structured data to text."""
    return (
        f"{company.get('name')} | Industry: {company.get('industry')} | "
        f"Size: {company.get('headcount')} | Tech: {', '.join(company.get('tech_stack', []))} | "
        f"{company.get('description', '')}"
    )


def chunk_blog_post(text: str, chunk_size: int = 200, overlap: int = 50) -> list[str]:
    """Paragraph-level chunking with token overlap for blog content."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i : i + chunk_size]))
        i += chunk_size - overlap
    return chunks


def chunk_email(email: dict) -> str:
    """Email history: one chunk per email with outcome metadata."""
    return (
        f"To: {email.get('recipient')} | Subject: {email.get('subject')} | "
        f"Outcome: {email.get('outcome', 'unknown')} | {email.get('body', '')}"
    )
