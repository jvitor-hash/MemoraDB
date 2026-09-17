from .executor import Executor, SimpleQueryExecutor
from .prepared import PreparedStatementManager
from .portals import PortalManager
from protocol.constants import (
    QUERY,
    PARSE,
    BIND,
    EXECUTE,
    TERMINATE,
)


class MessageDispatcher:
    
    def __init__(self, writer):
        self.writer = writer
        
        self.executor = Executor()
        self.simple_query = SimpleQueryExecutor(self.executor)
        
        self.prepared = PreparedStatementManager()
        self.portals = PortalManager()
        
    def dispatch(self, message_type, payload):
        if message_type == QUERY:
            return self.handle_query(payload)
            
        elif message_type == PARSE:
            return self.handle_parse(payload)
            
        elif message_type == BIND:
            return self.handle_bind(payload)
            
        elif message_type == EXECUTE:
            return self.handle_execute(payload)
            
        elif message_type == TERMINATE:
            return self.handle_terminate(payload)
            
        print(f"[?] Unknown message: {message_type!r}")
        return True
    
    def handle_query(self, payload):
        query = payload.rstrip(b"\x00").decode("utf-8")
        print(f"[QUERY] {query}")
        
        result = self.simple_query.execute(query)
        
        print(result)
        
        return True
        
    def handle_parse(self, payload):
        print(f"[PARSE] {payload!r}")
        
    def handle_bind(self, payload):
        print(f"[BIND] {payload!r}")

    def handle_execute(self, payload):
        print(f"[EXECUTE] {payload!r}")

    def handle_terminate(self, payload):
        print("[TERMINATE]")
        return False
