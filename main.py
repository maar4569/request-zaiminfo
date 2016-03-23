# coding: utf-8
import datetime
import codecs
import json
import zaim
from requestZaim.config.setting import configureRequestZaim
from requestZaim.oauth import ZaimAuth
from util.util import History
from util.util import Counter
import os.path
import sys
import time

if __name__ == "__main__":
    print 'requestZaimInfo start!'
    config = configureRequestZaim()
    history = History(config[u'historypath'])
    counter = Counter()

    date =  datetime.datetime.today()
    today_ymd = date.strftime('%Y-%m-%d')
    start_date = (date + datetime.timedelta(days=-62)).strftime('%Y-%m-%d')

    print 'start_date is {0}'.format(start_date)
    try:
        #outputfile
	basename = os.path.basename(config[u'outputjsonpath'])
        dirname = os.path.dirname(config[u'outputjsonpath'])
        today_ymdhms = date.strftime('%Y%m%d%H%M%S')
	name,ext = os.path.splitext(basename)
	filename = '{0}/{1}_{2}{3}'.format(dirname,name,today_ymdhms,ext)
        #fp = open(config[u'outputjsonpath'],'w')
        fp = open(filename,'w')
        fp = codecs.lookup('utf-8')[-1](fp)

        #authentication
        zauth = ZaimAuth(config)
        if zauth.do() != 0:
            sys.exit(1)
        print 'authentication success!!'
        #requests 
        zapi = zaim.ExtendedApi(consumer_key=config[u'consumer'][u'key'], \
	                        consumer_secret=config[u'consumer'][u'secret'], \
                                access_token=zauth._oauth_token, \
                                access_token_secret=zauth._oauth_token_secret
			       )
        categories = zapi.search_category()[u'categories']
        for category in categories:

	    genres = zapi.search_genre(category_id=category[u'id'])[u'genres']
	    for genre in genres:
	        moneys = zapi.search(category_id=category[u'local_id'], \
		    	             genre_id=genre[u'local_id'], \
			    	     start_date=start_date,\
				     end_date=today_ymd, \
				     mode='payment')['money']

	        for money in moneys:
		    if history._last_epoch_t < history._to_epoch(str(money[u'created'])):
                        json_str = json.dumps(money,ensure_ascii=False)
	                print json_str   
		        fp.write(json_str + '\n')
		        counter.up()
                        history.updateLastCreated(str(money[u'created']))
                    else:
		        print 'skipped. (already processed) id={0} created={1}'.format(money[u'id'],money[u'created'])
                history.write()
            print '{0} events found.'.format(str(counter.value()))
        fp.close()
    except IOError as e:
	print e
    except Exception as e:
        print e
    finally:
        fp.close()


    
