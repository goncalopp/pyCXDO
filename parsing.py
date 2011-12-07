from BeautifulSoup import BeautifulSoup

class ParsingError( Exception ):
    pass

def get_cxdo_version(html):
    '''Get the cxdo site version on all pages'''
    B1= "<!-- CXDO: "
    B2= " -->"
    try:
        i= html.index(B1)+len(B1)
        j= html.index(B2, i)
        return html[i:j]
    except:
        raise ParsingError("Could not detect CXDO site version")

def get_accounts( html):
    '''gets a dict with accounts indexes, labels on ORDEM_STATEMENT, PRAZO_STATEMENT'''
    soup= BeautifulSoup(html)
    fieldset=   soup.find('fieldset')
    if not fieldset:
        raise ParsingError()
    options=    fieldset.div.select.findAll("option")
    values=     [ option['value'] for option in options ]
    labels=     [ option.string for option in options ]
    return dict(zip(labels, values))

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
