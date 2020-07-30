import re
import sys
import requests
from .logger import logger
from .get_file import get_file

def _soap_call(args, payload):
    headers = {'content-type': 'application/soap+xml'}
    #headers = {'content-type': 'text/xml'}
    r = requests.post(
        args["wsdl_api_url"],
        data=payload,
        headers=headers
    )
    return r.status_code, r.text

def soap_call(args, template, regex):
    template = get_file(template)
    payload = template.format(**args)
    logger.debug("Payload:\n %s"%payload)

    status_code, response = _soap_call(args, payload)

    if status_code != 200:
        logger.error("The status code returned is %d"%status_code)
        sys.exit(1)
    
    logger.debug("Complete response:\n%s"%response)

    regex = get_file(regex)
    logger.debug("Extracting the result with :\n%s"%regex)

    results = re.findall(regex, response)
    logger.debug("Result with :\n%s"%results)

    if results:
        return results[0]