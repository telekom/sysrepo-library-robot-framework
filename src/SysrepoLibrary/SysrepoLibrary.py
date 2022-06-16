from robot.api.deco import library, keyword

import sysrepo


@library(scope='GLOBAL')
class SysrepoLibrary(object):
    """
    SysrepoLibrary is a Robot Framework library for Sysrepo.
    """

    def __init__(self):
        self.conns = {}
        self.sessions = {}

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

        :datastore:
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
            yangData = ctx.parse_data_mem(data, fmt, no_state=True, strict=True)

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
