#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import msgpack
import requests
from io import BytesIO

from MetasploitMethods import MetasploitMethods as MsfMethod

class MetasploitSession(object):
    _host = None
    _token = None

    def __init__(self, username, password, host):
        self._host = host
        self._username = username
        self._password = password

    def __enter__(self):
        resp = self.authenticate(self._username, self._password)

        if 'error' in resp:
            raise Exception(resp['error_message'])
        if resp['result'] == 'success':
            self._token = resp['token']

    def authenticate(self, username, password):
        return self.execute(MsfMethod.AuthLogin, username, password)

    def execute(self, method, *args):
        if method != MsfMethod.AuthLogin and self._token is None:
            raise Exception('Not authenticated')

        send_token = (not self._token is None) and (method != MsfMethod.AuthLogin) 
        headers = {'Content-Type': 'binary/message-pack'}

        if send_token:
            data_pkt = msgpack.packb(self._token) 
        else:
            pkt = [method]
            pkt.extend(args)
            data_pkt = msgpack.packb(pkt)

        r = requests.post(
            self._host,
            headers=headers,
            data=data_pkt
        )

        resp = msgpack.unpackb(r.content)
        return resp

    def __exit__(self):
        if not self._token is None:
            self.execute(MsfMethod.AuthLogout, self._token)
            self._token = None
