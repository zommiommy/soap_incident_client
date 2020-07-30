import sys
import time
import requests
from urllib.parse import quote
from .utils import logger

def acknowledge(args):
    url = "{neteye_url}/v1/actions/acknowledge-problem".format(**args)
    logger.info("[AK] acknowledgin host %s on url %s"%(args["host"], url))
    headers = {
        'Accept': 'application/json',
    }
    data = {
        "type": "Service",
        "filter": "host.name==\"%s\" && match(\"%s\", service.name)"%(args["host"], args["service"]),
        "author": args["author"],
        "comment": args["comment"].format(**args)
    }
    # Do the post
    r = requests.post(
        url,
        headers=headers,
        auth=(args["neteye_user"], args["neteye_password"]),
        json=data,
        verify=args["verify"]
    )

    logger.info("[AK] Status code %d:\n%s"%(r.status_code, r.text))
    if r.status_code == 200:
        logger.info("[AK] OK : %s"%r.json())
        return r.json()
    elif r.status_code in [500, 503, 404]:
        logger.error("[AK] got error: %s"%r.json())