def read_markdown_file(file_path: str) -> str:
    """
    Reads the content of a Markdown file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        raise

def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """
    Splits text into chunks with a specified size and overlap.
    """
    if not text:
        return []

    # Ensure chunk_overlap is not greater than chunk_size - 1
    # If it is, effectively set it to chunk_size - 1 to avoid negative step in range
    chunk_overlap = min(chunk_overlap, chunk_size - 1) if chunk_size > 0 else 0

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        if end >= len(text):
            break
        start += chunk_size - chunk_overlap
    return chunks