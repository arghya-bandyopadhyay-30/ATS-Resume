from docx import Document
from docx.opc.exceptions import PackageNotFoundError

def extract_text_from_docx(filepath: str) -> str:
    """
    Extract and return the text content from a .docx file as a single string.
    Only non-empty, stripped paragraphs are joined by newlines.
    Handles invalid or corrupted files gracefully.

    Args:
        filepath: Path to the .docx file.

    Returns:
        Cleaned text content of the document.

    Raises:
        ValueError: If the file is not a valid .docx or is corrupted.
    """
    try:
        document = Document(filepath)
        return '\n'.join(
            para.text.strip() for para in document.paragraphs if para.text and para.text.strip()
        )
    except PackageNotFoundError:
        raise ValueError(f"The file at '{filepath}' is not a valid .docx file or is corrupted.")
    except Exception as e:
        raise ValueError(f"An error occurred while reading the .docx file: {e}") 