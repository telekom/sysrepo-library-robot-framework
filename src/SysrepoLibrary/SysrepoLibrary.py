#
# telekom / sysrepo-plugin-system
#
# This program is made available under the terms of the
# BSD 3-Clause license which is available at
# https://opensource.org/licenses/BSD-3-Clause
#
# SPDX-FileCopyrightText: 2023 Deutsche Telekom AG
# SPDX-FileContributor: Sartura Ltd.
#
# SPDX-License-Identifier: BSD-3-Clause
#

from robot.api.deco import library, keyword

import sysrepo
import libyang
import json
import xmltodict


@library(scope='GLOBAL')
class SysrepoLibrary(object):
    """
    SysrepoLibrary is a Robot Framework library for Sysrepo.
    """

    def __init__(self):
        self.conns = {}
        self.sessions = {}
        self.FORMATS = {
            "xml": "XML",
            "json": "JSON"
        }

    @keyword("Open Sysrepo Connection")
    def open_connection(self):
        """
        Opens a Sysrepo connection.

        :returns:
            the connection ID of an opened connection
        """
        conn = sysrepo.SysrepoConnection()
        connID = 0
        if len(self.conns.keys()) != 0:
            connID = max(self.conns.keys()) + 1

        self.conns[connID] = conn
        self.sessions[connID] = dict()
        return connID

    @keyword("Close Sysrepo Connection")
    def close_connection(self, connID):
        """
        Closes a Sysrepo Connection.

        :arg connID:
            An opened connection ID.
        """
        if connID not in self.conns.keys():
            raise RuntimeError(f"Non-existing index {connID}")
        self.conns[connID].disconnect()
        del self.sessions[connID]

    @keyword("Open Datastore Session")
    def open_session(self, connID, datastore):
        """
        Opens a Sysrepo datastore session.

        :arg connID:
            An opened connection ID.

        :arg datastore:
            Specifies which datastore to open a session to.
            Example: "running"

        :returns:
            An open session ID.
        """
        if connID not in self.conns.keys():
            raise RuntimeError(f"Non-existing index {connID}")
        sess = self.conns[connID].start_session(datastore)

        sessID = 0
        if len(self.sessions[connID].keys()) != 0:
            sessID = max(self.sessions[connID].keys()) + 1

        self.sessions[connID][sessID] = sess

        return sessID

    @keyword("Close Datastore Session")
    def close_session(self, connID, sessID):
        """
        Closes a Sysrepo datastore session.

        :arg connID:
            An opened connection ID.
        :arg sessID:
            An opened session ID, corrseponding to the connection ID.
        """
        if connID not in self.conns.keys():
            raise RuntimeError(f"Non-existing connection index {connID}")

        if sessID not in self.sessions[connID]:
            raise RuntimeError(f"Non-existing session index {sessID}")

        self.sessions[connID][sessID].stop()
        del self.sessions[connID][sessID]

    @keyword("Close All Sysrepo Connections And Sessions")
    def close_all_connections_and_sessions(self):
        """
        Closes all open connections and sessions.
        Example: for usage with `Suite Teardown`
        """
        # force a key copy, avoid runtime error for dicitionary len change
        for connID in tuple(self.conns):
            for sessID in tuple(self.sessions[connID]):
                self.close_session(connID, sessID)
            self.close_connection(connID)

    @keyword("Get Datastore Data")
    def get_datastore_data(self, connID, sessID, xpath, fmt):
        """
        Get a datastore's data.

        :arg connID:
            An opened connection ID.
        :arg sessID:
            An opened session ID, corresponding to the connection.
        :arg xpath:
            The datastore's XML path
        :arg fmt:
            Format of the returned data.
            Example: xml

        :returns:
            The datastore's data in the specified format.
        """
        if connID not in self.conns.keys():
            raise RuntimeError(f"Non-existing connection index {connID}")

        if sessID not in self.sessions[connID]:
            raise RuntimeError(f"Non-existing session index {sessID}")

        with self.sessions[connID][sessID].get_data_ly(xpath) as data:
            return data.print_mem(fmt, pretty=False, with_siblings=True)

    @keyword("Edit Datastore Config")
    def edit_config(self, connID, sessID, data, fmt):
        """
        Edit a datastore's config file.

        :arg connID:
            An opened connection ID.
        :arg sessID:
            An opened session ID, corresponding to the connection.
        :arg data:
            The new config data
        :arg fmt:
            Format of the returned data.
            Example: xml
        """
        if connID not in self.conns.keys():
            raise RuntimeError(f"Non-existing connection index {connID}")

        if sessID not in self.sessions[connID]:
            raise RuntimeError(f"Non-existing session index {sessID}")

        with self.conns[connID].get_ly_ctx() as ctx:
            yangData = ctx.parse_data_mem(data,
                                          fmt,
                                          no_state=True,
                                          strict=True)

        self.sessions[connID][sessID].edit_batch_ly(yangData)
        self.sessions[connID][sessID].apply_changes()
        yangData.free()

    def xml_to_json(self, data: str) -> str:
        return json.dumps(xmltodict.parse(data))

    def is_json_empty(self, data: str) -> bool:
        jobj = json.loads(data)
        return jobj.length() == 0

    def is_data_empty(self, fmt: str, data: str) -> bool:
        is_empty = False

        if fmt != self.FORMATS["xml"] and fmt != self.FORMATS["json"]:
            raise RuntimeError(f"Non-supported format {fmt}")

        if fmt == self.FORMATS["xml"]:
            data = self.xml_to_json(data)

        if self.is_json_empty(data):
            is_empty = True

        return is_empty

    @keyword("Edit Datastore Config Safe")
    def edit_config_safe(self, connID, sessID, data, fmt, xpath):
        """
        Edit a datastore's config file.

        :arg connID:
            An opened connection ID.
        :arg sessID:
            An opened session ID, corresponding to the connection.
        :arg data:
            The new config data
        :arg fmt:
            Format of the returned data.
            Example: xml
        :arg xpath:
            xpath to delete if data is null
        """
        if connID not in self.conns.keys():
            raise RuntimeError(f"Non-existing connection index {connID}")

        if sessID not in self.sessions[connID]:
            raise RuntimeError(f"Non-existing session index {sessID}")

        if self.is_data_empty(data):
            self.sessions[connID][sessID].delete_item(xpath)

        with self.conns[connID].get_ly_ctx() as ctx:
            yangData = ctx.parse_data_mem(data,
                                          fmt,
                                          no_state=True,
                                          strict=True)

        self.sessions[connID][sessID].edit_batch_ly(yangData)
        self.sessions[connID][sessID].apply_changes()
        yangData.free()

    @keyword("Edit Datastore Config By File")
    def edit_config_by_file(self, connID, sessID, fpath, fmt):
        """
        Edit a datastore's config file by a file's contents.

        :arg connID:
            An opened connection ID.
        :arg sessID:
            An opened session ID, corresponding to the connection.
        :arg fpath:
            Path to the file containing the data.
        :arg fmt:
            Format of the returned data.
            Example: xml
        """
        if connID not in self.conns.keys():
            raise RuntimeError(f"Non-existing connection index {connID}")

        if sessID not in self.sessions[connID]:
            raise RuntimeError(f"Non-existing session index {sessID}")

        try:
            with open(fpath, "r") as f:
                data = f.read().strip()
                self.edit_config(connID, sessID, data, fmt)
        except IOError:
            raise RuntimeError(f"Non-existing file {fpath}")

    @keyword("Send RPC")
    def send_rpc(self, connID, rpc, fmt):
        """
        Send a RPC.

        :arg connID:
            An opened connection ID.
        :arg rpc:
            Rpc to send.
        :arg fmt:
            Format of the returned data.
            Example: xml

        :returns:
            The data in the specified format.
        """
        if connID not in self.conns.keys():
            raise RuntimeError(f"Non-existing connection index {connID}")

        with self.conns[connID].get_ly_ctx() as ctx:
            dnode = ctx.parse_op_mem(fmt, rpc, libyang.DataType.RPC_YANG)
            data = dnode.print(fmt, out_type=libyang.IOType.MEMORY)
            dnode.free()
            return data

    @keyword("Send RPC By File")
    def send_rpc_by_file(self, connID, fpath, fmt):
        """
        Send a RPC by a file's contents.

        :arg connID:
            An opened connection ID.
        :arg fpath:
            Path to the file containing the data.
        :arg fmt:
            Format of the returned data.
            Example: xml

        :returns:
            The data in the specified format.
        """
        if connID not in self.conns.keys():
            raise RuntimeError(f"Non-existing connection index {connID}")

        try:
            with open(fpath, "r") as f:
                rpc = f.read().strip()
                return self.send_rpc(connID, rpc, fmt)
        except IOError:
            raise RuntimeError(f"Non-existing file {fpath}")
