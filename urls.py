LOGINSTART=         "https://caixadirecta.cgd.pt/CaixaDirecta/loginStart.do"
LOGIN=              "https://caixadirecta.cgd.pt/CaixaDirecta/login.do"
MAIN=               "https://caixadirecta.cgd.pt/CaixaDirecta/profile.do"
ORDEM_STATEMENT=    "https://caixadirecta.cgd.pt/CaixaDirecta/globalStatement.do"
PRAZO_STATEMENT=    "https://caixadirecta.cgd.pt/CaixaDirecta/savingsBalance.do"

import cxdo_auth, misc
import datetime


#each of the following functions returns a tuple with (url, post_data). 
#url is a string.
#post_data is a dictionary string->string
#Optionally, a boolean is added to indicate if the request is expected to be redirected

def login_start( username ):
    return LOGINSTART, {"USERNAME":username}

def login( login_start_page_html, username, password):
    auth_data= cxdo_auth.parameters(login_start_page_html, username,password) 
    return LOGIN, auth_data, True

def main():
    return MAIN,

def ordem_statement():
    return ORDEM_STATEMENT,

def prazo_statement():
    return PRAZO_STATEMENT,

def get_movements_file(account_index, start_date, end_date, ordem=True, format="tsv"):
    '''cIdParam=LLsMLsD&channelIdAs=statement.do&statementKey=1323276889093&filter=&refresh=&moreResults=&nextPageId=&accountLabel=conta_a_ordem&accountIndex=2&changeActiveAccount=0&periodValues=4&startDate.day=7&startDate.month=11&startDate.year=2011&startDate.wasChanged=1&startDate.hour=16&startDate.minute=54&endDate.day=7&endDate.month=12&endDate.year=2011&endDate.wasChanged=1&endDate.hour=16&endDate.minute=54&totalBalance=725.54&availableBalance=717.56'''
    assert format in  ('tsv','csv')
    assert isinstance(start_date, datetime.datetime)
    assert isinstance(end_date,   datetime.datetime)
    base_url= ORDEM_STATEMENT if ordem else PRAZO_STATEMENT
    parameters= \
        {
        "accountIndex": account_index,
        "download": "globalStatement."+format,
        "downloadTypeP": format,
        "changeActiveAccount" : 1,
        "periodValues": -1
        }
    parameters.update( misc.datetime_to_post_format(start_date, "startDate."))
    parameters.update( misc.datetime_to_post_format(end_date,   "endDate."))
    return base_url, parameters
