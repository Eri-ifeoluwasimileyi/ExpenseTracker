class ExpenseNotFoundError(Exception):
    #when an expense with a given ID is not found
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


class NotEnoughBalanceError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code



class NoUpdatesFoundError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


class NoInfoFoundError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code
