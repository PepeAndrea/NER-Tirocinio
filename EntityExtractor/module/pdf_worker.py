import os
import pdftotext
import PyPDF2
from PyPDF2 import PdfReader
import sys


def get_pdf_pages(file):
    try:
        with open(file, "rb") as f:
            pdf = pdftotext.PDF(f)
        return pdf, os.path.basename(f.name)
    except FileNotFoundError:
        print("File not found! Please, update file path.")
        exit(1)


def _print_chapter(pdfreader, chapters, prefix=""):
    for chapter in chapters:
        if hasattr(chapter, "title"):
            pageNum = PyPDF2.PdfFileReader.getDestinationPageNumber(pdfreader, chapter)
            print(prefix + chapter.title, "--------- p:", pageNum + 1)
        else:
            _print_chapter(pdfreader, chapter, prefix=prefix + "\t")


def get_chapter(file):
    try:
        reader = PdfReader(file)
        _print_chapter(reader, reader.getOutlines())
    except IndexError:
        print("Paramentro mancante")
    except FileNotFoundError:
        print("Il file indicato non è stato trovato")
    except PyPDF2.errors.PdfReadError:
        print("File non valido")
