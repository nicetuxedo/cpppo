#! /usr/bin/env python

# 
# Poll a simple CIP device IP (or DNS name) "<hostname>" (default: localhost)
# 
#     poll_example_simple.py <hostname>
# 
import logging
import sys
import time
import threading

from cpppo.server.enip import poll
from cpppo.server.enip.get_attribute import proxy_simple as device

hostname			= sys.argv[1] if len( sys.argv ) > 1 else 'localhost'
values				= {} # { <parameter>: (<timer>, <value>), ... }
poller				= threading.Thread(
    target=poll.poll, args=(device,), kwargs={ 
        'address': 	(hostname, 44818),
        'cycle':	1.0,
        'timeout':	0.5,
        'process':	lambda par,val: values.update( { par: val } ),
        'params':	[('@1/1/1','INT'),('@1/1/7','SSTRING')],
    })
poller.daemon			= True
poller.start()

# Monitor the values dict (updated in another Thread)
while True:
    while values:
        logging.warning( "%16s == %r", *values.popitem() )
    time.sleep( .1 )

