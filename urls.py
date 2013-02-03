BASE=               "https://caixadirectaonline.cgd.pt"
LOGINSTART=         BASE+"/cdo/login.seam"
LOGIN=              BASE+"/cdo/auth/forms/login.fcc"
MAIN=               BASE+"/cdo/private/home.seam"
ORDEM_STATEMENT=    BASE+"/cdo/private/contasaordem/consultaSaldosMovimentos.seam"
PRAZO_STATEMENT=    BASE+"/cdo/private/poupancas/consultaSaldosMovimentosPoupanca.seam"

import misc
import datetime
import urllib


#each of the following functions returns a tuple with (url, post_data). 
#url is a string.
#post_data is a dictionary string->string
#Optionally, a boolean is added to indicate if the request is expected to be redirected

def login_start( username ):
    return LOGINSTART, {"USERNAME":username}

def login( login_start_page_html, username, password):
    params= {"username":"CDO"+username, "password":password, "target": MAIN[len(BASE):]}
    return LOGIN, params, True

def main():
    return MAIN,


def account_statement( ordem=True ):
    base_url= ORDEM_STATEMENT if ordem else PRAZO_STATEMENT
    parameters={}
    return base_url, parameters


def get_movements_file( account_page_html ):
    '''for this call to work correctly, one must first change the page 
    to the account statement page, and set its html as argument here'''
    ac_values, ac_labels, ac_selected= get_accounts( account_page_html )
    consultaMovimentos=consultaMovimentos
