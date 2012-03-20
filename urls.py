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


def account_statement( account_index= None, ordem=True, start_date=None, end_date=None):
    base_url= ORDEM_STATEMENT if ordem else PRAZO_STATEMENT
    parameters={}
    if account_index:
        parameters.update(
            {
            "accountIndex": account_index, 
            "changeActiveAccount" : 1,
            })
        if start_date and end_date:
            assert isinstance(start_date, datetime.datetime)
            assert isinstance(end_date,   datetime.datetime)
            parameters.update(
                {
                "periodValues": -1,
                })
            parameters.update( misc.datetime_to_post_format(start_date, "startDate."))
            parameters.update( misc.datetime_to_post_format(end_date,   "endDate."))
    return base_url, parameters


def get_movements_file( ordem, start_date=None, end_date=None, format="tsv"):
    '''for this call to work correctly, one must first change the page to the account statement page'''
    '''cIdParam=LLsMLsD&channelIdAs=statement.do&statementKey=1323276889093&filter=&refresh=&moreResults=&nextPageId=&accountLabel=conta_a_ordem&accountIndex=2&changeActiveAccount=0&periodValues=4&startDate.day=7&startDate.month=11&startDate.year=2011&startDate.wasChanged=1&startDate.hour=16&startDate.minute=54&endDate.day=7&endDate.month=12&endDate.year=2011&endDate.wasChanged=1&endDate.hour=16&endDate.minute=54&totalBalance=725.54&availableBalance=717.56'''
    assert format in  ('tsv','csv')
    base_url= ORDEM_STATEMENT if ordem else PRAZO_STATEMENT
    parameters= \
        {
        "download": "globalStatement."+format,
        "downloadTypeP": format,
        "periodValues": -1,
        "changeActiveAccount" : 0,
        }
    parameters.update( misc.datetime_to_post_format(start_date, "startDate."))
    parameters.update( misc.datetime_to_post_format(end_date,   "endDate."))

    return base_url, parameters
