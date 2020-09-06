class BadRequest(Exception):
    def __init__(self, key=None, message=None):
        super().__init__({
            "code": 400,
            "message": message,
            f"{key}": message
        })


class InternalError(Exception):
    def __init__(self, key=None, message=None):
        super().__init__({
            "code": 500,
            "message": message,
            f"{key}": message
        })


class NotFound(Exception):
    def __init__(self, key=None, message=None):
        super().__init__({
            "code": 404,
            "message": message,
            f"{key}": message
        })
