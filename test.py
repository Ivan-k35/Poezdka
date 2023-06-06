from zeep import Client
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport

url = "http://dev.avibus.pro/UEEDev/ws/SchedulePort?wsdl"
username = "wsuser"
password = "sales"

session = Session()
session.auth = HTTPBasicAuth(username, password)
client = Client(wsdl=url, transport=Transport(session=session))

resp = client.service.GetBusStops()
print(resp)
# methods = dir(client.service)
#
# print(methods)