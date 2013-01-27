import urllib, urllib2
import cxdo_auth, parsing, urls
import cookielib
import logging

CXDO_VERSION= "1.0.64.7  - "

class RedirectedException( Exception ):
    pass
class AuthenticationException( Exception):
    pass
class UnauthenticatedException( Exception ):
    pass
class SiteVersionMismatch( Exception ):
    pass


class Session(object):
    '''transparently performs authentication when necessary, keeps cookie file'''
    ENFORCE_VERSION= True  #enforce site version
    def __init__(self, user, password, cookie_file=None):
        self.cookie_file= cookie_file
        try:
            self._load_session()
        except (UnauthenticatedException, IOError):
            #file doesn't exist or cookie has expired
            self._new_session()
            self._authenticate(user, password)

    def _new_session(self):
        self.cookiejar= cookielib.LWPCookieJar()
        self.opener= urllib2.build_opener( urllib2.HTTPCookieProcessor(self.cookiejar) )

    def _load_session(self):
        self._new_session()
        self.cookiejar.load( filename= self.cookie_file, ignore_discard=True)
        logging.debug("cookie loaded from file")
        if not self._check_is_authenticated():
            raise UnauthenticatedException("saved cookie session has expired")
        

    def _save_session(self):
        logging.debug("saving cookie to file")
        if self.cookie_file is None:
            raise Exception("Cookie filename was not specified on construction")
        self.cookiejar.save( filename= self.cookie_file, ignore_discard=True)

    def _check_is_authenticated(self):
        try:
            html= self.get_page( *urls.account_statement() )
            return True
        except (UnauthenticatedException, RedirectedException):
            return False

    def _authenticate(self, user, password):
        logging.debug("authenticating...")
        try:
            assert type(user)==type(password)==str
            assert len(user)==7
            assert len(password)==6
        except AssertionError:
            raise Exception("Wrong user/password parameters")
        l1_html= self.get_page( *urls.login_start(user), check_authentication=False ) #needed to set cookies?
        l2_html= self.get_page( *urls.login(l1_html, user,password), check_authentication=False)
        if not self._check_is_authenticated():
            raise AuthenticationException("Could not authenticate with given data")
        if not self.cookie_file is None:
            self._save_session()


    def get_page(self, url, parameters={}, allow_redirects=False, detect_version=True, check_authentication=True):
        logging.debug("get page {0}?{1}".format(url,parameters))
        d= urllib.urlencode(parameters)
        f= self.opener.open(url, data=d)
        if not allow_redirects and f.geturl()!=url:
            raise RedirectedException("got "+f.geturl()+" instead of "+url)
        html= f.read()
        if check_authentication:
            if parsing.session_expired(html):
                raise UnauthenticatedException("Session Expired")
        if detect_version:
            site_version= parsing.get_cxdo_version(html)
            if not CXDO_VERSION in site_version:
                tmp= "CXDO site version differs from expected. got '{0}', expected '{1}'".format(site_version, CXDO_VERSION)
                if Session.ENFORCE_VERSION:
                    raise SiteVersionMismatch( tmp )
                else:
                    logging.warn( tmp )
        return html
