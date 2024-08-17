class SuccessList:
    MESSAGES = {
        "login_success": "Uspesno ste se prijavili. Dobrodosli!",
        "logout_success": "Uspesno ste se odjavili, dodjite nam opet.",
        "update": "Uspesno ste izvrsili izmennu podataka.",
        "tepih_saved": "Uspesno ste uneli informacije.",
        "uspesno":"Uspesno ste sacuvali dnevni izvestaj."

    }
    
    @classmethod
    def get(cls, success_key: str) -> str:
        if success_key in cls.MESSAGES:
            return cls.MESSAGES[success_key]
        return "Unknown message. Please contact server administrator."