# coding: utf-8

REQUEST_ZAIM_CONFIG={
    'url': {
        'request_token':'https://api.zaim.net/v2/auth/request',	    
        'authorize':'https://auth.zaim.net/users/auth',	    
        'access_token':'https://api.zaim.net/v2/auth/access',	    
        'callback':'https://api.zaim.net',	    
     },
     'consumer':{
        'key':'yourkey',
	'secret':'yoursecret',
     },
     'zaimlogin':{
	'account':'youraccount',
	'passcode':'yourpasscode',
     },
     'historypath': 'history.txt',
     'outputjsonpath': './allexpenses.json',

}

def configureRequestZaim():
    return REQUEST_ZAIM_CONFIG




