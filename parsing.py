from BeautifulSoup import BeautifulSoup

class ParsingError( Exception ):
    pass

class CXDOTemporaryError( Exception ):
    pass

def get_cxdo_version(html):
    '''Get the cxdo site version on all pages'''
    B1= 'http-equiv="PCEVer" content="'
    B2= '"'
    try:
        i= html.index(B1)+len(B1)
        j= html.index(B2, i)
        return html[i:j]
    except:
        raise ParsingError("Could not detect CXDO site version")

def get_javax_viewstate(html):
    soup= BeautifulSoup(html)
    inpt= soup.find("input",  name="javax.faces.ViewState")
    if not inpt:
        raise ParsingError()
    return inpt['value']

def get_calendar_inputfields(html):
    soup= BeautifulSoup(html)
    fields= soup.findAll( "input", class="inputCalendarField")
    if not fields:
        raise ParsingError()
    import pdb; pdb.set_trace()
    return a,b IDS!

def get_accounts( html):
    '''gets a dict with accounts indexes, labels on ORDEM_STATEMENT, PRAZO_STATEMENT'''
    soup= BeautifulSoup(html)
    fieldset=   soup.find("select", id='consultaMovimentos:selectedAccount')
    if not fieldset:
        raise ParsingError()
    options=    fieldset.findAll("option")
    values=     [ option['value'] for option in options ]
    labels=     [ option.string for option in options ]
    import pdb;pdb.set_trace()
    selected=   0
    return values, labels, selected

def session_expired( html ):
    return "mainArea_center_unAuth" in html

"""
def get_statement_key(html)
    '''gets the statement_key on ORDEM_STATEMENT, PRAZO_STATEMENT'''
    #statement_key seems to be the server unix time, with milliseconds
    soup= BeautifulSoup(html)
    sk= soup.find("input", name="statementKey")
    if not sk:
        raise ParsingError()
    return sk['value']
"""
