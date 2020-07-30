import json
import argparse
from .soap_client import SOAPClient

def client():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--settings", help="Path to the settings json", type=str, default="./settings.json")
    parser.add_argument("-d", "--debug", help="Debug mode, print the xml generated and received", action="store_true", default=False)

    login_settings = parser.add_argument_group('login settings')
    login_settings.add_argument("identId", help="", type=str, nargs ='+', action = 'store')
    login_settings.add_argument("password", help="", type=str, nargs ='+', action = 'store')
    login_settings.add_argument("prozess", help="", type=str, nargs ='+', action = 'store')
    search_settings = parser.add_argument_group('search settings')
    search_settings.add_argument("label_monitoring", help="", nargs ='+', action = 'store', type=str)
    search_settings.add_argument("it_short_desc", help="", nargs ='+', action = 'store', type=str)
    insert_settings = parser.add_argument_group('insert settings')
    insert_settings.add_argument("se_severity", help="", nargs ='+', action = 'store', type=str)
    insert_settings.add_argument("inquiry_txt", help="", nargs ='+', action = 'store', type=str)

    args = vars(parser.parse_args())

    with open(args["settings"], "r") as f:
        settings = json.load(f)

    for k, v in args.items():
        if type(v) == list:
            args[k] = " ".join(v)

    args["host"] = args["label_monitoring"]
    args["service"] = args["it_short_desc"]

    print(args)

    SOAPClient(settings).run(args)