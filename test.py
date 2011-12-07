import logging
from cxdo_session import CXDOSession

COOKIE_FILE= "cookie.txt"
CONTRACT= "1234567"
PASSWORD= "123456"

logging.basicConfig(level=logging.DEBUG)
session = CXDOSession(CONTRACT, PASSWORD, COOKIE_FILE)
print "Sucessfull authentication on CXDO!"
