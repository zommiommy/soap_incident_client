import json
import argparse
from .soap_client import SOAPClient

def client():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--settings", help="Path to the settings json", type=str, default="./settings.json")
    parser.add_argument("-d", "--debug", help="Debug mode, print the xml generated and received", action="store_true", default=False)

    login_settings = parser.add_argument_group('login settings')
    login_settings.add_argument("identId", help="", type=str)
    login_settings.add_argument("password", help="", type=str)
    login_settings.add_argument("prozess", help="", type=str)
    search_settings = parser.add_argument_group('search settings')
    search_settings.add_argument("label_monitoring", help="", type=str)
    search_settings.add_argument("it_short_desc", help="", type=str)
    insert_settings = parser.add_argument_group('insert settings')
    insert_settings.add_argument("se_severity", help="", type=str)
    insert_settings.add_argument("inquiry_txt", help="", type=str)
    acknow_settings = parser.add_argument_group('acknowledge settings')
    acknow_settings.add_argument("host", help="", type=str)
    acknow_settings.add_argument("service", help="", type=str)

    args = vars(parser.parse_args())

    with open(args["settings"], "r") as f:
        settings = json.load(f)

    print(args)

    SOAPClient(settings).run(args)