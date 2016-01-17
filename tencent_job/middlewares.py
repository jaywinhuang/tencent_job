__author__ = 'jaywinhuang'

import base64

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://web-proxy.oa.com:8080"