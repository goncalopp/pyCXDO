import session, urls, parsing, transactions
import datetime

class CXDOConnectedObject( object ):
    '''a base class that has a CXDOConnection as an attribute'''
    def __init__(self, connection):
        assert isinstance(connection, CXDOConnection)
        self.connection= connection

class Account( CXDOConnectedObject ):
    PRAZO, ORDEM= "prazo", "ordem"
    '''this class represents an bank account'''
    def __init__(self, name, index, account_type, *args):
        CXDOConnectedObject.__init__(self, *args)
        self.name= name
        self.index= index
        self.account_type= account_type
        
    def getBalance(self):
        '''gets the current account balance'''
        raise NotImplementedError()

    def getName( self ):
        return self.name

    def getIndex (self ):
        return self.index

    def getAccountNumber(self):
        raise NotImplementedError()

    def _fetch_transactions(self):
        start_date= datetime.datetime(year=2009, month=1, day=1)
        end_date= datetime.datetime.utcnow()
        file_str= self.connection.get_movements_file( self.index, start_date, end_date, self.account_type==Account.ORDEM)
        self.transactions= transactions.parse_tsv( file_str)

    def getTransactions( self ):
        if not hasattr(self, "transactions"):
            self._fetch_transactions()
        return self.transactions.transactions

class CXDOConnection( session.Session ):
    '''this class contains high level methods to fetch information from the site'''
    def get_ordem_accounts(self):
        html= self.get_page( *urls.ordem_statement() )
        return parsing.get_accounts(html)

    def get_prazo_accounts(self):
        html= self.get_page( *urls.prazo_statement() )
        return parsing.get_accounts(html)
    
    def get_movements_file(self, account_index, start_date, end_date, ordem=True, format='tsv'):
        html= self.get_page( *urls.get_movements_file( account_index, start_date, end_date, ordem, format), detect_version=False)
        return html

class CXDO( CXDOConnectedObject ):
    '''This is the main CXDO class. It caches results and only uses a CXDOConnection to communicate with CXDO when necessary'''
    def __init__(self, username, password, cookie_file=None):
        CXDOConnectedObject.__init__(self, CXDOConnection(username, password, cookie_file))

    def _fetch_accounts(self):
        c=self.connection
        accounts= \
            [ Account(name, index, Account.ORDEM, self.connection) for name,index in c.get_ordem_accounts().items() ] + \
            [ Account(name, index, Account.PRAZO, self.connection) for name,index in c.get_prazo_accounts().items()]
        self.accounts= dict( [(a.getName(), a) for a in accounts])
            
    def list_accounts(self):
        '''lists accounts by name'''
        if not hasattr(self, "accounts"):
            self._fetch_accounts()
        return self.accounts.keys()

    def getAccount( self, name ):
        if not hasattr(self, "accounts"):
            self._fetch_accounts()
        return self.accounts[name]
