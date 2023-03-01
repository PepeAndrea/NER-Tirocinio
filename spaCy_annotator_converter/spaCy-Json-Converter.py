import getopt
import json
import sys

import spacy
from spacy.tokens import DocBin
from tqdm import tqdm

argumentList = sys.argv[1:]

# Options
options = "i:o:"

# Long options
long_options = ["input=", "output="]

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:

        if currentArgument in ("-i", "--input"):
            input_file_path = currentValue
        elif currentArgument in ("-o", "--output"):
            output_path = currentValue

except getopt.error as err:
    # output error, and return with an error code
    print(str(err))

nlp = spacy.blank("en")  # Load a new spacy model
db = DocBin()  # Create a DocBin object

json_file = open(input_file_path)

# Prepare output path
output_file_name = json_file.name.split("/")[-1][:-5]+".spacy"
output_path = output_path+"/"+output_file_name

TRAINING_DATA = json.load(json_file)

for text, annotations in tqdm(TRAINING_DATA['annotations']):
    doc = nlp.make_doc(text)
    ents = []
    for start, end, label in annotations["entities"]:
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            print("Skipping entity")
        else:
            ents.append(span)
    doc.ents = ents
    db.add(doc)


db.to_disk(output_path)  # Save the DocBin object
