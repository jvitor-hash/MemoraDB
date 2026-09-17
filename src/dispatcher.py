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
from protocol.messages import (
    Query
)


class MessageDispatcher:
    
    def __init__(self, writer):
        self.writer = writer
        
        self.executor = Executor()
        self.simple_query = SimpleQueryExecutor(self.executor, self.writer)
        
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
        message = Query.decode(payload)
        print(f"[QUERY] {message.query}")
        
        result = self.simple_query.execute(message.query)
        
        print(result)
        
        return True
        
    def handle_parse(self, payload):
        print(f"[PARSE] {payload!r}")
        return True
        
    def handle_bind(self, payload):
        print(f"[BIND] {payload!r}")
        return True

    def handle_execute(self, payload):
        print(f"[EXECUTE] {payload!r}")
        return True

    def handle_terminate(self, payload):
        print("[TERMINATE]")
        return False
