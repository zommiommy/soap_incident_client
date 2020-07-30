import sys
import json
import argparse
from .soap_client import SOAPClient

def client():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--settings", help="Path to the settings json", type=str, default="./settings.json")
    parser.add_argument("-d", "--debug", help="Debug mode, print the xml generated and received", action="store_true", default=False)

    parser.add_argument("identId", help="", type=str)
    parser.add_argument("password", help="", type=str)
    parser.add_argument("prozess", help="", type=str)
    parser.add_argument("label_monitoring", help="", type=str)
    parser.add_argument("it_short_desc", help="", type=str)
    parser.add_argument("se_severity", help="", type=str)
    parser.add_argument("inquiry_txt", help="", type=str)
    args = vars(parser.parse_args())

    with open(args["settings"], "r") as f:
        settings = json.load(f)

    args["host"] = args["label_monitoring"]
    args["service"] = args["it_short_desc"]

    if args["debug"]:
        print("Argument received by the client:\n%s"%args)

    SOAPClient(settings).run(args)