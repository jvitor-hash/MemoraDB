from .database import USERS
from protocol.constants import (
    ROW_DESCRIPTION,
    DATA_ROW,
    COMMAND_COMPLETE,
    READY_FOR_QUERY
)
from protocol.messages import (
    row_description,
    data_row,
    command_complete
)

class SimpleQueryExecutor:
    
    def __init__(self, executor, writer):
        self.executor = executor
        self.writer = writer
        
    def execute(self, query: str):
        result = self.executor.execute(query)
        
        self.writer.send_message(
            ROW_DESCRIPTION,
            row_description(result["columns"])
        )
        
        for row in result["rows"]:
            self.writer.send_message(
                DATA_ROW,
                data_row(row)
            )
            
        self.writer.send_message(
            COMMAND_COMPLETE,
            command_complete(len(result["rows"]))
        )
        
        self.writer.send_message(
            READY_FOR_QUERY,
            b"I"
        )
        

class Executor:
    
    def execute(self, query: str, params=None):
        query = query.strip().rstrip(";")
        
        if query.lower() == "select * from users":
            return {
                "columns": ["id", "name"],
                "rows": [
                    [user["id"], user["name"]]
                    for user in USERS
                ],
            }
            
        raise ValueError(f"Unsupported query: {query}")