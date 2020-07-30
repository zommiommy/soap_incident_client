
import zeep
from zeep import xsd
from lxml import etree as ET

def dict_to_obj(kwargs, tag):
    seq = xsd.Sequence([
        xsd.Element(key, xsd.String())
        for key in kwargs.keys()
    ])
    if tag is None:
        return xsd.AnyObject(seq, xsd.ComplexType(seq)(**kwargs))
    el = xsd.Element(tag, seq)
    return xsd.AnyObject(el, xsd.ComplexType(el)(kwargs))

# Esempio di chiamata
# node = client.create_message(client.service, "ProcessOperation", 
            # identId="identId",
            # password="password",
            # prozess="prozess",
            # version=1.0,
            # processData=dict_to_obj(en="a", it="b")
# )
# Result:
# <soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">
#   <soap-env:Body>
#     <ns0:ProcessOperation xmlns:ns0="http://www.iet-solutions.de/">
#       <ns0:identId>identId</ns0:identId>
#       <ns0:password>password</ns0:password>
#       <ns0:prozess>prozess</ns0:prozess>
#       <ns0:version>1.0</ns0:version>
#       <ns0:processData>
#         <en>a</en>
#         <it>b</it>
#       </ns0:processData>
#     </ns0:ProcessOperation>
#   </soap-env:Body>
# </soap-env:Envelope>