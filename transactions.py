# -*- coding: utf-8 -*-
import datetime

class ParsingError( Exception ):
    pass

class Transaction(object):
    def __init__(self, date, amount_date, amount, description):
        assert isinstance(date, datetime.datetime)
        assert isinstance(amount_date, datetime.datetime)
        assert type(amount)==float
        self.date= date
        self.amount_date= amount_date
        self.amount= amount
        self.description= description
    
    def __repr__(self):
        return "{0} {1:10.2f}  {2}".format(self.date.strftime("%Y-%m-%d"), self.amount, self.description)

    def __eq__(self, other):
        return self.description==other.description and self.amount==other.amount and self.date==other.date and self.amount_date==other.amount_date

class AccountTransactions( object ):
    EUR= "EUR"
    def __init__( self, account_name, currency, transactions, balance_at_last_transaction ):
        assert currency in (AccountTransactions.EUR,)
        assert all ( [isinstance(x, Transaction) for x in transactions])
        assert sorted(transactions, reverse=True, key=lambda x:x.date)==transactions  #are reverse sorted by date 
        self.account_name= account_name
        self.currency= currency
        self.transactions= transactions
        self.balt= balance_at_last_transaction
    
    def merge( self , other):
        '''merges two AccountTransactions into a single one, deleting duplicate transactions, etc'''
        assert isinstance( other, AccountTransactions )
        if self.account_name!=other.account_name:
            raise Exception("Trying to merge transactions from two different accounts")
        try:
            i= other.transactions.index( self.transactions[0] )
            transactions= other.transactions[:i] + self.transactions
            last_balance= other.balt
        except ValueError:
            try:
                i= self.transactions.index( other.transactions[0] )
                transactions= self.transactions[:i] + other.transactions
                last_balance= self.balt
            except ValueError:
                raise Exception("transactions do not seem to overlap. cannot find cut point")
        if len(transactions)<max(len(self.transactions), len(other.transactions)):
            raise Exception("Error. may occurr when one transaction list is (totally) contained by the other")
        return AccountTransactions( self.account_name, self.currency, transactions, last_balance) 
    
    def __repr__( self ):
        s="Transactions on account {0} ({1})".format(self.account_name, self.currency)
        s+= "\n\t"+"\n\t".join(map(str, self.transactions))
        return s



def parse_tsv(tsv_string):
    '''parses CXDO tsv transactions file contents'''
    if type(tsv_string)!=unicode:
        tsv_string= tsv_string.decode('iso-8859-1')
    tsv_string= tsv_string.replace("\r\n","\n")
    lines= tsv_string.split("\n")
    assert lines[4]=="Movimentos"
    l= lines[6].split("\t")
    assert l[0]=="Conta"
    account_name= l[1]
    l= lines[7].split("\t")
    assert l[0]=="Moeda"
    currency= l[1]
    currency= l[1]
    assert lines[11]=="Data mov.	Data valor	Descrição	Débito	Crédito	Saldo contabilístico".decode('utf-8')
    assert lines[12]==""
    transactions= [parse_tsv_transaction(line) for line in lines[13:-6]]
    assert lines[-4].startswith("Saldo contabilístico".decode('utf-8'))
    assert lines[-2].startswith("Saldo disponível".decode('utf-8'))
    last_balance= float(lines[-4].split("\t")[1].replace(".","").replace(",","."))
    return AccountTransactions( account_name, currency, transactions, last_balance)
    
def parse_tsv_transaction(line):
    def parse_date( d ):
        return datetime.datetime.strptime( d, "%d-%m-%Y")
    s= line.split("\t")
    assert len(s)==6
    transaction_date=   parse_date(s[0])
    amount_date=        parse_date(s[1])
    description=        s[2]
    if s[3]:
        assert not s[4]
        amount= -float(s[3].replace(".","").replace(",","."))
    else:
        amount= float(s[4].replace(".","").replace(",","."))
    funds= s[5]
    return Transaction( transaction_date, amount_date, amount, description)


o= open("tmp.1")
s1= o.read()
o= open("tmp.2")
s2= o.read()
a1= parse_tsv(s1)
a2= parse_tsv(s2)
x= a1.merge(a2)
print x.balt
