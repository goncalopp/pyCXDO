# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup

SERVICE_UNAVAILABLE_MESSAGE=u"O Serviço encontra-se temporariamente indisponível. Pedimos desculpa pelo incómodo."


class ParsingError( Exception ):
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

def fix_html_inside_html(html):
    i=html.index("<html")
    while True:
        try:
            i=html.index("<html", i+1)
            i2= html.index(">", i)
            i3= html.index("</html>", i)
            html= html[:i]+html[i2+1:i3]+html[i3+7:]
        except ValueError:
            break
    return html

def get_form_input_values(html, form_id, field_name_attribute="name", filter_out_attributes=[]):
    '''get form fields and current values'''
    #if a tag has a attribute matching any of filter_out_attributes, it will not be parsed
    html= fix_html_inside_html(html) #sad, CGD, sad
    soup= BeautifulSoup(html)
    form= soup.find("form", id=form_id)
    form_values={}
    for field in form.findAll("input"):
        if field.get('type')=="submit":
            #the form submission button. It's not actual  form field
            continue
        field_name= field.get(field_name_attribute)
        if field_name:
            #we don't parse any fields where we can't get the field name
            field_value= field.get('value') or ""
            form_values[field_name]= field_value
    for field in form.findAll("select"):
        field_name= field.get(field_name_attribute)
        if field_name:
            #we don't parse any fields where we can't get the field name
            field_value= get_form_selected_value(field)
            form_values[field_name]= field_value
    return form_values

def get_form_selected_value( select_tag ):
    '''given a <select> tag, returns the value of the selected option'''
    selected= [o for o in select_tag.findAll("option") if o.get('selected')=='selected']
    if len(selected)!=1:
        raise Exception("Can't find selected element (0 or many selected)")
    return selected[0]['value']

def get_calendar_inputfields(html):
    soup= BeautifulSoup(html)
    import pdb; pdb.set_trace()
    fields= soup.findAll( "input", **{"class": "inputCalendarField"})
    if not fields:
        raise ParsingError()
    import pdb; pdb.set_trace()
    return a,b

def get_accounts( html):
    '''gets a dict with accounts indexes, labels on ORDEM_STATEMENT, PRAZO_STATEMENT'''
    soup= BeautifulSoup(html)
    fieldset=   soup.find("select", id=lambda x: ':selectedAccount' in x)
    if not fieldset:
        raise ParsingError()
    options=    fieldset.findAll("option")
    #account names
    names=     [ option['value'] for option in options ]
    #account labels
    labels=     [ option.string for option in options ]
    #selected account name
    selected=   names.index(fieldset.find( "option", selected="selected")['value'])
    return names, labels, selected

def session_expired( html ):
    return "mainArea_center_unAuth" in html

def service_temporarily_unavailable( html ):
    soup= BeautifulSoup( html )
    login_error= soup.find("div", id="erroLoginMsgArea")
    if login_error:
        text= login_error.text
        if text==SERVICE_UNAVAILABLE_MESSAGE:
            return True
    return False
    

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
