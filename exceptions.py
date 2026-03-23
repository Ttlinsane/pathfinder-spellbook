class UserError(ValueError):
    http_status: int = 400
    def __init__(self,message:str,code: str | None = None, field:str|None=None, http_status:int|None=None):
        super().__init__(message)
        self.code = code
        self.field = field
        if http_status is not None:
            self.http_status = http_status
    @property
    def user_message(self):
        return str(self)
    
    def to_dict(self):
        return {"message":self.user_message, "code":self.code,"field":self.field, "http_status":self.http_status}

class EmptyItem(UserError):
    http_status=400
    def __init__(self):
        super().__init__("用户名或密码不能为空", code="username_password", field="username_password")

class PasswordTooShort(UserError):
    http_status=400
    def __init__(self):
        super().__init__("密码太短", code="password_too_short", field="password")

class NameCoincidence(UserError):
    http_status=400
    def __init__(self):
        super().__init__("用户名重复", code="name_coincidence", field="username")

__all__ = ["UserError","EmptyItem","PasswordTooShort","UserError","NameCoincidence"]
#补完计划：路由层

