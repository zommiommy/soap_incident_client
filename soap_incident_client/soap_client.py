import re
import sys
from requests import Session
from .acknowledge import acknowledge
from .utils import soap_call, logger

def soap_client(args):
    incident_id = soap_call(args, "search.xml", "search_regex.txt")
    if incident_id is None:
        args["incident_id"] = soap_call(args, "insert.xml", "insert_regex.txt")
        #acknowledge(ack_args)
    else:
        soap_call(args, "update.xml", "update_regex.txt")

