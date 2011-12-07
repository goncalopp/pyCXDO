import logging
from cxdo import CXDO

COOKIE_FILE= "cookie.txt"
CONTRACT= "1234567"
PASSWORD= "123456"

logging.basicConfig(level=logging.DEBUG)
cxdo = CXDO(CONTRACT, PASSWORD, COOKIE_FILE)
print "Sucessfull authentication on CXDO!"
