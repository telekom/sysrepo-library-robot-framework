import sysrepo

class SysrepoLibrary:
    """SysrepoLibrary is a Robot Framework library for Sysrepo.
    """
    ROBOT_LIBRARY_SCOPE="GLOBAL"
    ROBOT_LIBRARY_VERSION=__version__

    def __init__(self):
        self.conns = {}
        self.sessions = {}

    @keyword
    def open_connection(self):
        conn = sysrepo.SysrepoConnection()
        connID = 0
        if len(self.conns.keys()) != 0:
            connID = max(self.conns.keys()) + 1

        conns[connID] = conn
        self.sessions[connID] = dict()
        return connID

    @keyword
    def close_connection(self, connID):
        if connID not in self.conns.keys():
            raise RuntimeError(f"Non-existing index {connID}")
        self.conns[connID].disconnect()
        del self.sessions[connID]

    @keyword
    def open_session(self, connID, datastore):
        if connID not in self.conns.keys():
            raise RuntimeError(f"Non-existing index {connID}")
        sess = self.conns[connID].start_session(datastore)

        sessID = 0
        if len(self.sessions[connID].keys()) != 0:
            sessID = max(self.sessions[connID].keys()) + 1
        self.sessions[connID][sessID] = sess

        return sessID

    @keyword
    def close_session(self, connID, sessID):
        if connID not in self.conns.keys():
            raise RuntimeError(f"Non-existing connection index {connID}")

        if sessID not in self.sessions[connID]:
            raise RuntimeError(f"Non-existing session index {sessID}")

        self.sessions[connID][sessID].stop()
        del self.sessions[connID][sessID]

    @keyword
    def edit_config(self, connID, sessID, data, fmt):
        if connID not in self.conns.keys():
            raise RuntimeError(f"Non-existing connection index {connID}")

        if sessID not in self.sessions[connID]:
            raise RuntimeError(f"Non-existing session index {sessID}")

        ctx = self.conns[connID].get_ly_ctx()
        yangData = ctx.parse_data_mem(data, fmt, config=True, strict=True)
        self.sessions[connID][sessID].edit_batch_ly(yangData)
        data.free()
        self.sessions[connID][sessID].apply_changes()
