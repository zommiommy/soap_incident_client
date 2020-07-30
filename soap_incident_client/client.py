import json
import argparse
from .soap_client import SOAPClient

def client():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--settings", help="Path to the settings json", type=str, default="./settings.json")
    parser.add_argument("-d", "--debug", help="Debug mode, print the xml generated and received", action="store_true", default=False)

    login_settings = parser.add_argument_group('login settings')
    login_settings.add_argument("-i", "--identId", help="", type=str, required=True)
    login_settings.add_argument("-pw", "--password", help="", type=str, required=True)
    login_settings.add_argument("-p", "--prozess", help="", type=str, required=True)
    search_settings = parser.add_argument_group('search settings')
    search_settings.add_argument("-l", "--label_monitoring", help="", type=str, required=True)
    search_settings.add_argument("-sd", "--it_short_desc", help="", type=str, required=True)
    insert_settings = parser.add_argument_group('insert settings')
    insert_settings.add_argument("-se", "--se_severity", help="", type=str, required=True)
    insert_settings.add_argument("-it", "--inquiry_txt", help="", type=str, required=True)

    args = vars(parser.parse_args())

    with open(args["settings"], "r") as f:
        settings = json.load(f)

    args["host"] = args["label_monitoring"]
    args["service"] = args["it_short_desc"]

    print(args)

    SOAPClient(settings).run(args)