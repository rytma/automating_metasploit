#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from MetasploitMethods import MetasploitMethods as MsfMethod

class MetasploitManager(object):
    def __init__(self, session):
        self._session = session

    def __exit__(self):
        self._session = None

    def list_jobs(self):
        return self._session.execute(MsfMethod.JobList)

    def stop_job(self, job_id):
        return self._session.execute(MsfMethod.JobStop, job_id)

    def exec_module(self, module_type, module_name, options):
        return self._session.execute(MsfMethod.ModuleExec, module_type, module_name, options)

    def list_sessions(self):
        return self._session.execute(MsfMethod.SessionList)

    def stop_session(self, session_id):
        return self._session.execute(MsfMethod.SessionStop, session_id)

    def read_session_shell(self, session_id, read_pointer):
        if read_pointer is None:
            return self._session.execute(MsfMethod.SessionShellRead, session_id)
        return self._session.execute(MsfMethod.SessionShellRead, session_id, read_pointer)

    def write_session_shell(self, session_id, data):
        return self._session.execute(MsfMethod.SessionShellWrite, session_id, data)
