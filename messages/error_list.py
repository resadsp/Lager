class ErrorList:
    ERRORS = {
        "invalid_credentials": "Userneme ili password nisu tacni.",
        "invalid_password": "Password nije tacan. Pokusajte ponovo.",
        "something": "Ne postoji tepih sa datom sifrom.",
        "vec_postoji": "Tepih sa datom sifrom vec postoji."
    }
    
    @classmethod
    def get(cls, error_key: str) -> str:
        if error_key in cls.ERRORS:
            return cls.ERRORS[error_key]
        return "Unknown error. Please contact server administrator."