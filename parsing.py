from BeautifulSoup import BeautifulSoup

class ParsingError( Exception ):
    pass

def get_cxdo_version(html):
    '''Get the sxdo site version. Available in all pages'''
    B1= "<!-- CXDO: "
    B2= " -->"
    try:
        i= html.index(B1)+len(B1)
        j= html.index(B2, i)
        return html[i:j]
    except:
        raise ParsingError("Could not detect CXDO site version")

def get_accounts( html):
    '''given the html from ORDEM_STATEMENT or PRAZO_STATEMENT urls, gets the accounts labels'''
    soup= BeautifulSoup(html)
    fieldset=   soup.find('fieldset')
    if not fieldset:
        import pdb;pdb.set_trace()
        raise ParsingError()
    options=    fieldset.div.select.findAll("option")
    values=     [ option['value'] for option in options ]
    labels=     [ option.string for option in options ]
    return labels

def session_expired( html ):
    return "mainArea_center_unAuth" in html
