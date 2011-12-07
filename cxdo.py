import session, urls, parsing

class CXDO( session.Session ):
    def get_ordem_accounts():
        html= self.get_page( urls.ordem_statement() )
        return parsing.get_ordem_accounts(html)
