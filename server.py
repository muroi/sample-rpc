#!/usr/bin/env python
# coding: utf-8

from oslo_config import cfg
import oslo_messaging as messaging
import oslo_messaging.rpc as rpc
import logging
import time
import sys

import eventlet

eventlet.monkey_patch()

logging.basicConfig()
log = logging.getLogger()

log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)


class ServerControlEndpoint(object):
    target = messaging.Target(namespace='congress-rpc', version='1.0')

    def __init__(self, server):
        self.server = server
        self.service_name = 'rpc_server'

    def stop(self, ctx):
        if self.server:
            self.server.stop()

class BaseAPI(object):
    
    def ping(self, context, arg):
        for i in range(1, 3):
            time.sleep(3)
            print 'ping called with %s, %s' % (arg, i)

    def cast_ping(self, context, arg):
        print 'cast_ping called with %s' % arg


def main(server_name):
    log.info('Configuring connection')
    transport_url = 'rabbit://testing:test@127.0.0.1:5672/'
    transport = messaging.get_transport(cfg.CONF, transport_url)


    targets = messaging.Target(topic='test', server=server_name)
    endpoints = [ServerControlEndpoint(None), BaseAPI()]

    server = messaging.get_rpc_server(transport, targets, endpoints, executor='blocking')

    log.info('Starting up server')
    server.start()
    log.info('Waiting for something')
    server.wait()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python server.py <server_name>'
        exit 0

    server_name = sys.argv[1]
    main(server_name)
        
