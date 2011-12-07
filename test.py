import logging
import datetime
from cxdo import CXDO

COOKIE_FILE= "cookie.txt"
CONTRACT= "1234567"
PASSWORD= "123456"

logging.basicConfig(level=logging.DEBUG)
cxdo = CXDO(CONTRACT, PASSWORD, COOKIE_FILE)
print "Sucessfull authentication on CXDO!"

contas_ordem = cxdo.get_ordem_accounts()
print "prazo accounts", contas_ordem.keys()

ordem_label= contas_ordem.keys()[0]
ordem_index= contas_ordem[ ordem_label ]
print "getting csv file of movements in account "+ordem_label
start= datetime.datetime(year=2011, month=1, day=1)
end= datetime.datetime(year=2011, month=12, day=21)

print cxdo.get_movements_file( ordem_index, start, end)
