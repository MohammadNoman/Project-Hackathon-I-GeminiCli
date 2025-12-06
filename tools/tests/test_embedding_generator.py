import pytest
from tools.embedding_generator import read_markdown_file

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
