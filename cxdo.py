import session, urls, parsing

class CXDO( session.Session ):
    def get_ordem_accounts(self):
        html= self.get_page( *urls.ordem_statement() )
        return parsing.get_accounts(html)

    def get_prazo_accounts(self):
        html= self.get_page( *urls.prazo_statement() )
        return parsing.get_accounts(html)
    
    def get_movements_file(self, account_index, start_date, end_date, ordem=True, format='tsv'):
        html= self.get_page( *urls.get_movements_file( account_index, start_date, end_date, ordem, format), detect_version=False)
        return html
