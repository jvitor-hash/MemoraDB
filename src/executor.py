from .database import USERS


class SimpleQueryExecutor:
    
    def __init__(self, executor):
        self.executor = executor
        
    def execute(self, query: str):
        return self.executor.execute(query)

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