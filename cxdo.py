import session, urls, parsing

class CXDO( session.Session ):
    def get_ordem_accounts(self):
        html= self.get_page( *urls.ordem_statement() )
        return parsing.get_accounts(html)

    def get_prazo_accounts(self):
        html= self.get_page( *urls.prazo_statement() )
        return parsing.get_accounts(html)
