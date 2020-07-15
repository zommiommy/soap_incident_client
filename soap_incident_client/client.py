import re
import sys
import json
import argparse
import logging
from .soap_client import soap_client
from .utils import setup_logger, logger

def client():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--settings", help="Path to the settings json", type=str, default="./settings.json")
    parser.add_argument("-v", "--verbosity", help="Log level, 0 = Warning, 1 = Info, 2 = Debug", type=int, default=0, choices=[0, 1, 2])

    parser.add_argument("identId", help="ITSM User Name", type=str)
    parser.add_argument("password", help="ITSM User Password", type=str)
    parser.add_argument("label_monitoring", help="ITSM CI Label Monitoring", type=str)
    parser.add_argument("it_short_desc", help="NetEye Service Object/Host Object Name", type=str)
    parser.add_argument("se_severity", help="NetEye Service Object/Host Object current Status", type=str, choices=("OK", "WARNING", "CRITICAL", "UNKNOWN"))
    parser.add_argument("inquiry_txt", help="Neteye Check Command Output", type=str)
    args = vars(parser.parse_args())

    with open(args["settings"], "r") as f:
        settings = json.load(f)

    args["host"] = args["label_monitoring"]
    args["service"] = args["it_short_desc"]
    args["shortdesc"] = args["it_short_desc"]

    setup_logger({
        0:logging.WARN,
        1:logging.INFO,
        2:logging.DEBUG
    }.get(args.pop("verbosity"), logging.WARN))
    logger.debug("Argument received by the client:\n%s"%args)

    settings.update(args)
    soap_client(settings)