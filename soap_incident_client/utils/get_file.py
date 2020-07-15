import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_file(filename):
    with open(os.path.join(ROOT, "configs", filename), "r") as f:
        return f.read()