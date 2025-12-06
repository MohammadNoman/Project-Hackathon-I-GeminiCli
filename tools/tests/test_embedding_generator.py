import pytest
from tools.embedding_generator import read_markdown_file, chunk_text

def test_read_markdown_file_exists(tmp_path):
    """
    Test that the read_markdown_file function can read an existing Markdown file.
    """
    # Create a dummy Markdown file
    file_content = "# Test Title\nThis is some test content."
    file_path = tmp_path / "test_file.md"
    file_path.write_text(file_content)

    # Call the function to read the file
    content = read_markdown_file(str(file_path))

    # Assert that the content is read correctly
    assert content == file_content

def test_read_markdown_file_non_existent():
    """
    Test that the read_markdown_file function raises FileNotFoundError for a non-existent file.
    """
    with pytest.raises(FileNotFoundError):
        read_markdown_file("non_existent_file.md")

def test_read_markdown_file_empty(tmp_path):
    """
    Test that the read_markdown_file function can read an empty Markdown file.
    """
    file_content = ""
    file_path = tmp_path / "empty_file.md"
    file_path.write_text(file_content)

    content = read_markdown_file(str(file_path))
    assert content == file_content

def test_chunk_text_simple_case():
    """
    Test that chunk_text splits a simple text into chunks correctly.
    """
    text = "This is a long sentence that needs to be chunked into smaller pieces."
    chunks = chunk_text(text, chunk_size=10, chunk_overlap=0)
    assert len(chunks) > 1
    assert all(len(chunk) <= 10 for chunk in chunks)
    assert chunks[0] == "This is a "
    assert chunks[1] == "long sente"

def test_chunk_text_with_overlap():
    """
    Test that chunk_text handles chunk overlap correctly.
    """
    text = "abcdefghij"
    chunks = chunk_text(text, chunk_size=5, chunk_overlap=2)
    assert chunks == ["abcde", "defgh", "ghij"] # Corrected expectation


def test_chunk_text_empty_input():
    """
    Test that chunk_text returns an empty list for empty input.
    """
    text = ""
    chunks = chunk_text(text, chunk_size=10, chunk_overlap=0)
    assert chunks == []

def test_chunk_text_chunk_size_greater_than_text_length():
    """
    Test that chunk_text returns a single chunk if chunk_size > text length.
    """
    text = "short text"
    chunks = chunk_text(text, chunk_size=20, chunk_overlap=0)
    assert chunks == ["short text"]



