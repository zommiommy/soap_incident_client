import re
import sys
from requests import Session
from .acknowledge import acknowledge
from .utils import soap_call, logger

def soap_client(args):
    incident_id = soap_call(args, "search.xml", "search_regex.txt")
    if incident_id is None:
        logger.info("No id found, executing an insert.")
        args["inquiryID"] = soap_call(args, "insert.xml", "insert_regex.txt")
        logger.info("Done insert on id %s"%args["inquiryID"])
        acknowledge(args)
    else:
        logger.info("Found the id %s, going to update it state."%incident_id)
        args["inquiryID"] = incident_id
        ident_id = soap_call(args, "update.xml", "update_regex.txt")
        logger.info("Done update on id %s"%ident_id)
        if args["se_severity"].strip().lower() != "ok":
            acknowledge(args)
    logger.info("Done!")
