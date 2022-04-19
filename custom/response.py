class Response():
    def __init__(self, status = "200 OK", body = ""):
        self.status = status
        self.body = body
        self.headers = {"Connection": "close"}

    """
    HTTP/1.1 200 OK
    Date: Sun, 10 Oct 2010 23:26:07 GMT
    Server: Apache/2.2.8 (Ubuntu) mod_ssl/2.2.8 OpenSSL/0.9.8g
    Last-Modified: Sun, 26 Sep 2010 22:04:35 GMT
    ETag: "45b6-834-49130cc1182c0"
    Accept-Ranges: bytes

    body of the respose
    """
    def format_response(self):
        response = f"HTTP/1.0 {self.status}\n"
        self.headers["Content-Length"] = len(self.body)
        for key, value in self.headers.items():
            response += f"{key}: {value}\n"
        response += "\n"
        response += self.body
        return response

