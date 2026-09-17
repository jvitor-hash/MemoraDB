class PortalManager:
    
    def __init__(self):
        self.portals = {}
        
    def bind(self, name: str, statement: str, params=None):
        self.portals[name] = {
            "statement": statement,
            "params": params or []
        }
        
    def get(self, name: str):
        return self.portals[name]
    
    def remove(self, name: str):
        self.portals.pop(name, None)