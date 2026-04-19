"""Smoke test — verify package imports correctly."""


def test_package_imports():
    import src
    assert src.__version__ == "0.1.0"


def test_chunker():
    from src.rag.chunker import chunk_blog_post

    text = " ".join(["word"] * 500)
    chunks = chunk_blog_post(text, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert all(len(c.split()) <= 100 for c in chunks)
