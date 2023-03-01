import os
import spacy
from spacy import displacy
import json
from threading import Thread


def store_html_output(documents, file_name):
    html = displacy.render(documents, style="ent", page=True)
    # Create the HTML file
    html_file = "".join([os.path.abspath("."), "/output/", file_name[:-3], "html"])
    with open(html_file, "w", encoding='ISO-8859-1', errors="xmlcharrefreplace") as f:
        f.write(html)
    return html_file


def _process_page(page, index, documents, nlp):
    doc = nlp(page)
    documents[index] = doc


def process_pdf(nlp, pages):
    n_pages = len(pages)
    documents = [None] * n_pages
    threads = []

    for i in range(n_pages):
        page = pages[i]
        thread = Thread(target=_process_page, args=(page, i, documents, nlp))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return documents


def setup_nlp(config):
    nlp = spacy.load(config["model"])
    if config["ruler_position"] is not None and config["ruler_patterns"] is not None:
        try:
            with open(config["ruler_patterns"], "r") as json_patterns:
                patterns = json.loads(json_patterns.read())
            if config["ruler_position"] == "after":
                ruler = nlp.add_pipe("entity_ruler", after="ner", config={"overwrite_ents": True})
            else:
                ruler = nlp.add_pipe("entity_ruler", before="ner")
            ruler.add_patterns(patterns)
        except (FileNotFoundError, FileNotFoundError, json.decoder.JSONDecodeError) as error:
            print(error)
            print("Non è stato possibile aggiungere il dizionario alla pipeline")

    return nlp
