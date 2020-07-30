from IPython import embed
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
        print("Raw xml message sent:\n%s"%ET.tostring(tree, pretty_print=True).decode())

    def _call(self, args, prozess, request_object): 
        kwargs = {
            "identId":args["identId"],
            "password":args["password"],
            "prozess":prozess,
            "version":1.0,
            "processData":dict_to_obj(request_object)
        }
        if args["debug"]:
            self._debug(kwargs)
            with self.client.settings(raw_response=True):
                r = self.client.service.ProcessOperation(**kwargs)
                print("Raw xml response %d:\n%s"%(r.status_code, r.content))
        return self.client.service.ProcessOperation(**kwargs)

    def search(self, args):
        result = self._call(args, self.settings["prozess_search"], {
            "it_short_desc":args["it_short_desc"],
            "label_monitoring":args["label_monitoring"],
        })
        if args["debug"]:
            print("Complete response:\n%s"%result)
            print("Decoded element:\n%s"%ET.tostring(result["Result"]["_value_1"]).decode())
            embed()
        if result["Status"] == "No Error":
            return None
        if result["Status"] != "Error":
            return result["Result"]["ident_id"]
        else:
            return None

    def insert(self, args):
        result = self._call(args, self.settings["prozess_insert"], {
            "it_short_desc":args["it_short_desc"],
            "label_monitoring":args["label_monitoring"],
            "inquiry_txt":args["inquiry_txt"],
            "se_severity":args["se_severity"],
        })
        if args["debug"]:
            print("Complete response:\n%s"%result)
            print("Decoded element:\n%s"%ET.tostring(result["Result"]["_value_1"]).decode())

        # TODO figure out how to extract the result inicdent id

    def update(self, args, incident_id):
        result = self._call(args, self.settings["prozess_update"], {
                "inquiry_id":args["inquiry_id"],
                "inquiry_txt":args["inquiry_txt"],
                "se_severity":args["se_severity"],
        })
        if self.settings["debug"]:
            print("Complete response:\n%s"%result)
            print("Decoded element:\n%s"%ET.tostring(result["Result"]["_value_1"]).decode())
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

