class GlobalComponents:
    COMPONENTS = {}
    
    @classmethod
    def set(cls, key: str, component: any):
        cls.COMPONENTS[key] = component 
        
    @classmethod
    def get(cls, key: str):
        return cls.COMPONENTS[key] if key in cls.COMPONENTS else None
    