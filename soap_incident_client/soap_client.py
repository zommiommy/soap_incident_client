
from zeep import xsd
from zeep import Client
from requests import Session
from zeep.transports import Transport
from .acknowledge import acknowledge

from lxml import etree as ET


class SOAPClient:
    """Client that handles the specific SOAP calls"""
    def __init__(self, settings):
        self.settings =  settings
        self.client = Client(settings["wsdl_path"])


    def _debug(self, args, request_object): 
        node = self.client.create_message(
            self.client.service,
            "ProcessOperation",
            identId=args["identId"],
            password=args["password"],
            prozess=args["prozess"],
            version=1.0,
            processData=request_object
        )
        tree = ET.ElementTree(node)
        print(ET.tostring(tree, pretty_print=True).decode())

    def _call(self, args, request_object): 
        return self.client.service.ProcessOperation(
            identId=args["identId"],
            password=args["password"],
            prozess=args["prozess"],
            version=1.0,
            processData=request_object
        )

    def search(self, args):
        result = self._debug(args, {
            "it_short_desc":args["it_short_desc"],
            "label_monitoring":args["label_monitoring"],
        })

        # TODO figure out how to extract the result inicdent id

    def insert(self, args):
        result = self._debug(args, {
            "shortdesc":args["it_short_desc"],
            "label_monitoring":args["label_monitoring"],
            "inquiry_txt":args["inquiry_txt"],
            "se_severity":args["se_severity"],
        })

        # TODO figure out how to extract the result inicdent id

    def update(self, args, incident_id):
        result = self._debug(args, {
                "inquiry_id":args["inquiry_id"],
                "inquiry_txt":args["inquiry_txt"],
                "se_severity":args["se_severity"],
        })
        # TODO parse the result

    def run(self, args):
        incident_id = self.search(args)
        if incident_id is None:
            args["incident_id"] = self.insert(args)
            acknowledge(args, self.settings)
        else:
            self.update(args, incident_id)

