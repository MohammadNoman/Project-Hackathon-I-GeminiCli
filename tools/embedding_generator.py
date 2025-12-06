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