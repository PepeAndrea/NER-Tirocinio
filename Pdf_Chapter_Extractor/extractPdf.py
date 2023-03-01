import PyPDF2
from PyPDF2 import PdfReader
import sys


def print_chapter(pdfreader, chapters, prefix=""):
    for chapter in chapters:
        if hasattr(chapter, "title"):
            pageNum = PyPDF2.PdfFileReader.getDestinationPageNumber(pdfreader, chapter)
            print(prefix + chapter.title, "--------- p:", pageNum + 1)
        else:
            print_chapter(pdfreader, chapter, prefix=prefix + "\t")


try:
    reader = PdfReader(sys.argv[1])
    print_chapter(reader, reader.getOutlines())
except IndexError:
    print("Paramentro mancante")
except FileNotFoundError:
    print("Il file indicato non è stato trovato")
except PyPDF2.errors.PdfReadError:
    print("File non valido")
