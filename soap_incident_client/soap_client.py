
from zeep import xsd
from zeep import Client
from requests import Session
from zeep.transports import Transport
from .acknowledge import acknowledge


class SOAPClient:
    """Client that handles the specific SOAP calls"""
    def __init__(self, args, settings):
        self.args, self.settings = args, settings
        self.client = Client(settings["wsdl_path"])
        self.client.setup_authentication_header(args)

    def setup_authentication_header(self, args):
        header = xsd.Element(
            'AuthenticationInfo',
            xsd.ComplexType([
                xsd.Element('identId',xsd.String()),
                xsd.Element('password',xsd.String())
            ])
        )
        self.header_value = [header(identId=args["identId"], password=args["password"])]

    def search(self):
        pass

    def insert(self):
        pass

    def update(self, incident_id):
        pass

    def run(self):
        incident_id = self.search()
        if incident_id is None:
            self.args["incident_id"] = self.insert()
            acknowledge(self.args, self.settings)
        else:
            self.update(incident_id)

