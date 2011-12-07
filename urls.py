LOGINSTART=         "https://caixadirecta.cgd.pt/CaixaDirecta/loginStart.do"
LOGIN=              "https://caixadirecta.cgd.pt/CaixaDirecta/login.do"
MAIN=               "https://caixadirecta.cgd.pt/CaixaDirecta/profile.do"
ORDEM_STATEMENT=    "https://caixadirecta.cgd.pt/CaixaDirecta/globalStatement.do"
PRAZO_STATEMENT=    "https://caixadirecta.cgd.pt/CaixaDirecta/savingsBalance.do"

import cxdo_auth


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
