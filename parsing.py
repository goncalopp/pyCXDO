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

