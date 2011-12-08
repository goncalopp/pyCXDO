import session, urls, parsing

class Account( object ):
    PRAZO, ORDEM= "prazo", "ordem"
    '''this class represents an bank account'''
    def __init__(self, name, index, account_type):
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
    
    def getTransactions( start_date, end_date ):
        raise NotImplementedError()

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

class CXDO( object ):
    '''This is the main CXDO class. It caches results and only uses a CXDOConnection to communicate with CXDO when necessary'''
    def __init__(self, username, password, cookie_file=None):
        self.connection= CXDOConnection(username, password, cookie_file)

    def list_accounts(self):
        '''lists accounts by name'''
        if not hasattr(self, "accounts"):
            c=self.connection
            self.accounts= \
                [ Account(name, index, Account.ORDEM) for name,index in c.get_ordem_accounts().items() ] + \
                [ Account(name, index, Account.ORDEM) for name,index in c.get_prazo_accounts().items()]
        return map(Account.getName, self.accounts)
