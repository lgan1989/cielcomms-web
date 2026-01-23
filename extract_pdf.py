#!/usr/bin/env python3
import subprocess
import sys
import os

pdf_path = "/Users/lugan/Personal/ciel-co/Ciel & Co. Communications_0123.pdf"

# Try pdftotext first
try:
    result = subprocess.run(
        ['pdftotext', '-layout', pdf_path, '-'],
        capture_output=True, text=True
    )
    if result.returncode == 0 and result.stdout.strip():
        print("=== PDF Content (pdftotext) ===")
        print(result.stdout)
        sys.exit(0)
except FileNotFoundError:
    pass

# Try using strings command as fallback
try:
    result = subprocess.run(
        ['strings', pdf_path],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("=== PDF Content (strings) ===")
        # Filter to get meaningful text
        lines = result.stdout.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) > 3 and not line.startswith('%') and not line.startswith('/'):
                print(line)
except Exception as e:
    print(f"Error: {e}")

# Try PyPDF2 if available
try:
    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_path)
    print("\n=== PDF Content (PyPDF2) ===")
    print(f"Number of pages: {len(reader.pages)}")
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        print(f"\n--- Page {i+1} ---")
        print(text)
except ImportError:
    print("PyPDF2 not installed")
except Exception as e:
    print(f"PyPDF2 error: {e}")
