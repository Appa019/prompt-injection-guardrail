"""Reads the receipt the way a naive agent would: plain text extraction, white text included."""

from pypdf import PdfReader

from expenses.config import ROOT

RECEIPT = ROOT / "data" / "receipt.pdf"


def read_receipt(path=RECEIPT):
    return "\n".join(page.extract_text() for page in PdfReader(path).pages)
