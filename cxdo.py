import urllib, urllib2
from BeautifulSoup import BeautifulSoup
import cxdo_auth
import cookielib
import logging

CXDO_VERSION= "v57_2_0_WS_v5_123_1"
LOGINSTARTPAGE= "https://caixadirecta.cgd.pt/CaixaDirecta/loginStart.do"
LOGINPAGE= "https://caixadirecta.cgd.pt/CaixaDirecta/login.do"
MAINPAGE= "https://caixadirecta.cgd.pt/CaixaDirecta/profile.do"

class RedirectedException( Exception ):
    pass
class AuthenticationException( Exception):
    pass
class UnauthenticatedException( Exception ):
    pass

def get_cxdo_version(html):
    B1= "<!-- CXDO: "
    B2= " -->"
    try:
        i= html.index(B1)+len(B1)
        j= html.index(B2, i)
        return html[i:j]
    except:
        logging.warn("Could not detect CXDO site version")
        return ""

class CXDO(object):
    def __init__(self, user, password, cookie_file=None):
        self.cookie_file= cookie_file
        try:
            self.load_session()
        except:
            #file doesn't exist or cookie has expired, etc
            self.authenticate(user, password)

        
    def get_page(self, url, parameters={}, allow_redirects=False):
        d= urllib.urlencode(parameters)
        f= self.opener.open(url, data=d)
        if not allow_redirects and f.geturl()!=url:
            raise RedirectedException("got "+f.geturl()+" instead of "+url)
        html= f.read()
        if not get_cxdo_version(html)==CXDO_VERSION:
            logging.warn("CXDO site version differs from expected. got'"+get_cxdo_version(html)+"', expected '"+CXDO_VERSION+"'")
        return html
        

    def new_session(self):
        self.cookiejar= cookielib.LWPCookieJar()
        self.opener= urllib2.build_opener( urllib2.HTTPCookieProcessor(self.cookiejar) )

    def load_session(self):
        self.new_session()
        self.cookiejar.load( filename= self.cookie_file, ignore_discard=True)
        logging.debug("cookie loaded from file")
        if not self.is_authenticated():
            raise UnauthenticatedException("saved cookie session has expired")
        

    def save_session(self):
        logging.debug("saving cookie to file")
        if self.cookie_file is None:
            raise Exception("Cookie filename was not specified on construction")
        self.cookiejar.save( filename= self.cookie_file, ignore_discard=True)

    def is_authenticated(self):
        try:
            html= self.get_page(MAINPAGE)
            return True
        except RedirectedException:
            return False

    def authenticate(self, user, password):
        logging.debug("authenticating...")
        try:
            assert type(user)==type(password)==str
            assert len(user)==7
            assert len(password)==6
        except:
            raise Exception("Wrong user parameter")

        
        l1_html= self.get_page( LOGINSTARTPAGE, {"USERNAME": user} ) #needed to set cookies?
        auth_data= cxdo_auth.parameters(l1_html, user,password) 
        l2_html= self.get_page( LOGINPAGE, auth_data, allow_redirects=True)
        if not self.is_authenticated():
            raise AuthenticationException("Could not authenticate with given data")
        if not self.cookie_file is None:
            self.save_session()
