class NotFoundError(Exception):
    def _init_(self, message="Resource not found"):
        self.message = message
        super()._init_(self.message)


class ValidationError(Exception):
    def _init_(self, message="Invalid input"):
        self.message = message
        super()._init_(self.message)