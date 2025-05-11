import pytest
from docx import Document
from src.backend.resume_parser.parser.reader import extract_text_from_docx

def create_docx(path, paragraphs):
    doc = Document()
    for p in paragraphs:
        doc.add_paragraph(p)
    doc.save(path)

def test_extract_text_success(tmp_path):
    # Create a .docx with two paragraphs
    docx_path = tmp_path / "test.docx"
    texts = ["Hello World", "  Second paragraph  "]
    create_docx(str(docx_path), texts)

    extracted = extract_text_from_docx(str(docx_path))
    # Leading/trailing whitespace should be stripped, empty lines removed
    assert extracted == "Hello World\nSecond paragraph"

def test_extract_text_invalid(tmp_path):
    # Create a fake (non-docx) file
    fake = tmp_path / "not_a_docx.docx"
    fake.write_text("I'm not a docx")
    with pytest.raises(ValueError) as exc:
        extract_text_from_docx(str(fake))
    assert "not a valid .docx file" in str(exc.value)
