class PreparedStatementManager:
    
    def __init__(self):
        self.statements = {}
        
    def parse(self, name: str, query: str):
        self.statements[name] = query
        
    def get(self, name: str):
        return self.statements[name]
    
    def remove(self, name: str):
        return self.statements.pop(name, None)