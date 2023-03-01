import getopt
import sys
from module.extractor_config import config
from module.extractor_config import validateConfig
import entity_extractor as ee

argumentList = sys.argv[1:]

# Short options
short_options = "f:m:b:a:s"
# Long options
long_options = ["file=", "model=", "dic-before=", "dic-after=", "serve"]

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, short_options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:

        if currentArgument in ("-f", "--file"):
            config["file"] = currentValue
        elif currentArgument in ("-m", "--model"):
            config["model"] = currentValue
        elif currentArgument in ("-b", "--dic-before"):
            config["ruler_position"] = "before"
            config["ruler_patterns"] = currentValue
        elif currentArgument in ("-a", "--dic-after"):
            config["ruler_position"] = "after"
            config["ruler_patterns"] = currentValue
        elif currentArgument in ("-s", "--serve"):
            config["serve"] = True

except getopt.error as err:
    # output error, and return with an error code
    print(str(err))

if validateConfig(config):
    ee.run(config)
else:
    print("Settings params not valid!")
