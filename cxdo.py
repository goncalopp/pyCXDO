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
    def __init__(self, name, label, index, account_type, *args):
        assert account_type in (self.PRAZO, self.ORDEM)
        CXDOConnectedObject.__init__(self, *args)
        self.name= name
        self.label= label
        self.index= index
        self.account_type= account_type
        
    def getBalance(self):
        '''gets the current account balance'''
        raise NotImplementedError()

    def getAccountNumber(self):
        raise NotImplementedError()

    def _fetch_transactions(self):
        start_date= datetime.datetime(year=2009, month=1, day=1)
        end_date= datetime.datetime.utcnow()
        file_str= self.connection.get_movements_file( self, start_date, end_date, self.account_type==Account.ORDEM)
        self.transactions= transactions.parse_tsv( file_str)

    def getTransactions( self ):
        if not hasattr(self, "transactions"):
            self._fetch_transactions()
        return self.transactions.transactions

    def __repr__(self):
        return "<Account({0}, {1})>".format(self.label, self.name)

class CXDOConnection( session.Session ):
    '''this class contains high level methods to fetch information from the site'''
    def get_ordem_accounts(self):
        html= self.get_page( *urls.account_statement( ordem= True) )
        return parsing.get_accounts(html)

    def get_prazo_accounts(self):
        html= self.get_page( *urls.account_statement( ordem=False) )
        return parsing.get_accounts(html)

    def get_account_page(self, account):
        '''navigates to an account page (marks it as selected...)'''
        ordem= (account.account_type==Account.ORDEM)
        html= self.get_page( *urls.account_statement( ordem=ordem ) )
        names, labels, selected= parsing.get_accounts(html)
        if selected==account.name:
            #the wanted account was the default one
            return html
        fields= parsing.get_form_input_values(html, "consultaMovimentos")
        import pdb; pdb.set_trace()
        self.get_page( urls.account_statement( ordem )[0], fields)

        
    def get_movements_file(self, account, start_date, end_date, ordem=True, format='tsv'):
        html= self.get_account_page( account )
        return html

class CXDO( CXDOConnectedObject ):
    '''This is the main CXDO class. It caches results and only uses a CXDOConnection to communicate with CXDO when necessary'''
    def __init__(self, username, password, cookie_file=None):
        CXDOConnectedObject.__init__(self, CXDOConnection(username, password, cookie_file))

    def _fetch_accounts(self):
        c=self.connection
        self.accounts=[]
        for accs, typ in (
                         (c.get_ordem_accounts(), Account.ORDEM), 
                         (c.get_prazo_accounts(), Account.PRAZO),
                          ):
            names, labels, selected= accs
            for i in range(len(names)):
                self.accounts.append( Account(names[i], labels[i], i, typ, self.connection) )

    def get_accounts(self):
        '''lists accounts by name'''
        if not hasattr(self, "accounts"):
            self._fetch_accounts()
        return self.accounts[:]

    def getAccount( self, s ):
        matches= [a for a in self.accounts if s in a.name or s in a.label]
        if len(matches)==0:
            raise Exception("No account matches")
        if len(matches)>1:
            raise Exception("Multiple account matches: "+str(matches))
        return matches[0]
