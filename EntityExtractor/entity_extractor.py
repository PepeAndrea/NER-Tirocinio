import platform
import subprocess
import sys
from module import pdf_worker as pw
from module import nlp_worker as nw
from time import time


def open_browser(url):
    system = platform.system()
    if system == "Windows":
        subprocess.Popen(["start", url], shell=True)
    elif system == "Darwin":
        subprocess.Popen(["open", url])
    else:
        subprocess.Popen(["xdg-open", url])


def run(config):
    START_TIME = time()
    pages, file_name = pw.get_pdf_pages(config["file"])
    print("Starting NLP task...")
    nlp = nw.setup_nlp(config)
    print("Processing data...")
    documents = nw.process_pdf(nlp, pages)
    print("Storing data...")
    output_path = nw.store_html_output(documents, file_name)
    if config["serve"] is True:
        open_browser(output_path)
    print(f"Processing complete in {round(time() - START_TIME, 2)} seconds!")
    sys.exit(0)

