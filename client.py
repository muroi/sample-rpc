#!/usr/bin/env python
# coding: utf-8

from oslo_config import cfg
import oslo_messaging as messaging

import logging

logging.basicConfig()
log = logging.getLogger()

log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

class TestClient(object):

    def __init__(self, transport, server_name, fanout=False):
        target = messaging.Target(topic='test', version='1.0', server=server_name, fanout=fanout)
        self._client = messaging.RPCClient(transport, target)

    def ping(self, ctxt, arg):
        print 'call'
        return self._client.call(ctxt, 'ping', arg=arg)


    def cast_ping(self, ctxt, arg):
        print 'cast'
        return self._client.cast(ctxt, 'cast_ping', arg=arg)


transport_url = 'rabbit://testing:test@127.0.0.1:5672/'
transport = messaging.get_transport(cfg.CONF, transport_url)

if len(sys.argv) != 2:
    print 'Usage: python client.py <server_name>'

server_name = sys.argv[1]
client = TestClient(transport, server_name, fanout=False)

print 'start call'
client.ping({'ctxt': 'aaa'}, {'arg1': 'value'})
print 'end call'

print 'start cast'
client.cast_ping({'ctxt': 'aaa'}, {'arg1': 'value'})
print 'end call'

client = TestClient(transport, server_name, fanout=True)

print 'start fanout call'
client.ping({'ctxt': 'aaa'}, {'arg1': 'value'})
print 'end call'

print 'start fanout cast'
client.cast_ping({'ctxt': 'aaa'}, {'arg1': 'value'})
print 'end call'

