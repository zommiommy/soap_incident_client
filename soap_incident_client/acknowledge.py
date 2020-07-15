import sys
import time
import logging
import requests
from urllib.parse import quote

def acknowledge(args):
    url = "{neteye_url}/v1/actions/acknowledge-problem".format(**args)
    logging.info("[AK] acknowledgin host %s on url %s"%(args["host"], url))
    headers = {
        'Accept': 'application/json',
    }
    data = {
        "type": "Service",
        "filter": "host.name==\"%s\" && match(\"%s\", service.name)"%(args["host"], args["service"]),
        "author": "ITSM",
        "comment": "Acknowledge by ITSM, incident_id: %s"%(args["incident_id"])
    }
    # Do the post
    r = requests.post(
        url,
        headers=headers,
        auth=(args["USER"], args["PW"]), verify=False,
        json=data,
    )

    if r.status_code == 200:
        logging.info("[AK] OK : %s"%r.json())
        return r.json()
    elif r.status_code in [500, 503, 404]:
        logging.error("[AK] got error: %s"%r.json())