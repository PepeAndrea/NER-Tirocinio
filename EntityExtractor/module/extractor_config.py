# Config array
config = {
    "file": None,
    "model": None,
    "ruler_position": None,
    "ruler_patterns": None,
    "serve": False
}


def validateConfig(configArray):
    if configArray["file"] is None or configArray["model"] is None:
        return False
    return True
