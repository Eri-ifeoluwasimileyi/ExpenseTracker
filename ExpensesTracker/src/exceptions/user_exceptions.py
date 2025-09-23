class UserNotFoundError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code

class UserAlreadyExistsError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


class InvalidAmountError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


class IncorrectPasswordError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code