import logging
import datetime
from cxdo import CXDO

COOKIE_FILE= "cookie.txt"
CONTRACT= "1234567"
PASSWORD= "123456"

logging.basicConfig(level=logging.DEBUG)
cxdo = CXDO(CONTRACT, PASSWORD, COOKIE_FILE)
print cxdo.list_accounts()
ordem= cxdo.getAccount("ordem")
t= ordem.getTransactions()
print t[0]
print t[-1]
