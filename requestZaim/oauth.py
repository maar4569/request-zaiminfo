# coding: utf-8
import mechanize
import urlparse
import requests
from requests_oauthlib import OAuth1
from bs4 import BeautifulSoup

class ZaimAuth(object):
    def __init__(self,oauth_config):
        self._oauth_config = oauth_config
        self._oauth_token=''
        self._oauth_token_secret=''
        self._oauth_verifier=''
	self._oauth_object=''
    def do(self):
	try:
            #try authentication , return callback url.
            br  = mechanize.Browser()
            br.open( self.__getAuthUrl() )
            br.select_form(nr=0)
            br['data[User][email]']    = self._oauth_config['zaimlogin']['account']
            br['data[User][password]'] = self._oauth_config['zaimlogin']['passcode']
            res = br.submit()
            scrayper = BeautifulSoup(res.read(), 'html.parser' )
            self._oauth_verifier = scrayper.find('code').next_element
            call_backurl = scrayper.find('div',{'class':'callback'}).next_element

            #get accesstoken
            print 'acccess_token=%s' % self.__getAccessToken()

            self._oauth_object = OAuth1(self._oauth_config['consumer']['key'],\
	                                self._oauth_config['consumer']['secret'], \
                                        self._oauth_token, \
                                        self._oauth_token_secret
            )
            return 0
	except Exception as e:
	    print e

    def __getAuthUrl(self):
        try:
            auth = OAuth1(self._oauth_config['consumer']['key'],\
			  self._oauth_config['consumer']['secret'], \
			  callback_uri=self._oauth_config['url']['callback']
			 )
            req  = requests.post(self._oauth_config['url']['request_token'], auth=auth)
            request_token = dict(urlparse.parse_qsl(req.text))
            self._oauth_token        = request_token['oauth_token']
            self._oauth_token_secret = request_token['oauth_token_secret']
            url= self._oauth_config['url']['authorize']+"?oauth_token=" + request_token["oauth_token"]
    
            return url

        except Exception as e:
	    print e

    def __getAccessToken(self):
        try:
            auth = OAuth1(self._oauth_config['consumer']['key'],\
			  self._oauth_config['consumer']['secret'], \
			  self._oauth_token, \
			  self._oauth_token_secret, \
			  verifier=self._oauth_verifier
			 )
            req    = requests.post(self._oauth_config['url']['access_token'] , auth=auth)
            token  = dict(urlparse.parse_qsl(req.text))
            self._oauth_token        = token['oauth_token']
            self._oauth_token_secret = token['oauth_token_secret']

            return 0
            
        except Exception as e:
	    print e


		    
