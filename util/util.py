import time
import json
import os.path
from datetime import datetime
class History(object):
    def __init__(self,historyfile):
	self._historyfile = historyfile
	if os.path.isfile(historyfile):
	    with open(historyfile , 'r') as f:
	        h_date = json.load(f)[u'history'].encode('UTF-8')
        else:
	    h_date = '1999-01-01 00:00:00'
        self._last_processed_date = self._str_to_date(h_date)
        self._last_epoch_t        = self._to_epoch(self._last_processed_date)
        self._next_processed_date = self._str_to_date(h_date)
        self._next_epoch_t        = self._to_epoch(self._next_processed_date)
	print 'last_processed_date {0}'.format(self._last_processed_date)
	print 'last_epoch_t {0}'.format(self._last_epoch_t)
	print 'next_processed_date {0}'.format(self._next_processed_date)
	print 'next_epoch_t {0}'.format(self._next_epoch_t)
    def write(self):
        with open(self._historyfile,'w' ) as f:
            json.dump({'history': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self._next_epoch_t))},\
			                        f,\
						sort_keys=True, \
						indent=4 \
					       )

    def _str_to_date(self,str_dt):
	'''
	   strdate to date.
	   input  date(type is str)
	   return date(type is time.struct_time)
	'''
        try:
            if isinstance(str_dt,str):
	        dt = time.strptime(str_dt,'%Y-%m-%d %H:%M:%S')
	    else:
                raise Exception
	    return dt
	except Exception as e:
	    print 'error={0}'.format(e)

    def _to_epoch(self,created_date):
	'''
	   date to epoch time.
	   input  date(type is str or time.struct_time)
	   return epoch time
	'''
	try:
            ep_t = ''
            if isinstance(created_date,str):
                ep_t = time.mktime(self._str_to_date(created_date))
	    elif isinstance(created_date,time.struct_time):
		ep_t = time.mktime(created_date)
            else:
		raise Exception
            return ep_t
        except Exception as e:
	    print '_tp_epoch error={0} input={1}'.format(e,created_date)

    def _epoch_to_dt(self,epoch_t):
        '''
	   epoch time to date format.
	   input  epoch time
	   return datetime(type struct_time))
	'''
	try:
            tmp = time.localtime(epoch_t)
	    dt = self._str_to_date(time.strftime('%Y-%m-%d %H:%M:%S', \
			                          time.localtime(epoch_t) \
				   ))
            return dt
        except Exception as e:
	    print e
      
    def updateLastCreated(self,created):
	'''
	    input created_time (type str or time.struct_time)
            return last_processed_date
	'''
        target_epoch_t = self._to_epoch(created)
	last_epoch_t = self._to_epoch(self._next_processed_date)
	self._next_epoch_t   = max(target_epoch_t,last_epoch_t)
        self._next_processed_date = self._epoch_to_dt(self._next_epoch_t)
        return self._next_processed_date


class Counter(object):
    def __init__(self):
        self._i=0

    def up(self):
        self._i = self._i + 1
	return self._i

    def value(self):
	return self._i
