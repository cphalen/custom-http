class HTTPException(Exception):
    def __init__(self, **kwargs):
        self.status_code = kwargs.get("status_code", 500)
        self.detail = kwargs.get("detail", "Internal Server Error")