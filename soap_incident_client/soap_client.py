
from zeep import xsd
from zeep import Client
from requests import Session
from zeep.transports import Transport
from .acknowledge import acknowledge
from .utils import dict_to_obj

from lxml import etree as ET


class SOAPClient:
    """Client that handles the specific SOAP calls"""
    def __init__(self, settings):
        self.settings =  settings
        self.client = Client(settings["wsdl_path"])

    def _debug(self, kwargs): 
        node = self.client.create_message(
            self.client.service, 
            "ProcessOperation",
            **kwargs
        )
        tree = ET.ElementTree(node)
        print(ET.tostring(tree, pretty_print=True).decode())

    def _call(self, args, request_object): 
        kwargs = {
            "identId":args["identId"],
            "password":args["password"],
            "prozess":args["prozess"],
            "version":1.0,
            "processData":dict_to_obj(request_object)
        }
        if args["debug"]:
            self._debug(kwargs)
        return self.client.service.ProcessOperation(**kwargs)

    def search(self, args):
        result = self._call(args, {
            "it_short_desc":args["it_short_desc"],
            "label_monitoring":args["label_monitoring"],
        })
        if args["debug"]:
            print(dir(result["Result"]._value_1))
            print(result["Result"]._value_1.text)
            print(result["Result"]._value_1.values)
            print(result["Result"]._value_1.keys)
        # TODO figure out how to extract the result inicdent id
        return result["Result"]

    def insert(self, args):
        result = self._call(args, {
            "shortdesc":args["it_short_desc"],
            "label_monitoring":args["label_monitoring"],
            "inquiry_txt":args["inquiry_txt"],
            "se_severity":args["se_severity"],
        })
        if args["debug"]:
            print(result)

        # TODO figure out how to extract the result inicdent id

    def update(self, args, incident_id):
        result = self._call(args, {
                "inquiry_id":args["inquiry_id"],
                "inquiry_txt":args["inquiry_txt"],
                "se_severity":args["se_severity"],
        })
        if self.settings["debug"]:
            print(result)
        # TODO parse the result

    def run(self, args):
        incident_id = self.search(args)
        if incident_id is None:
            args["incident_id"] = self.insert(args)
            ack_args = self.settings.copy()
            ack_args.update(args)
            acknowledge(ack_args)
        else:
            self.update(args, incident_id)

