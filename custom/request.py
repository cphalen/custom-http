import re
import json
from custom.exception import HTTPException
from json.decoder import JSONDecodeError


class Request:
    def __init__(self, message):
        self.headers = {}
        self.query_params = {}
        self.form_params = {}
        self.parse_http(message)

    """
    Example HTTP message
    ----------------------------------------------
    POST /hello.htm HTTP/1.1
    User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
    Host: www.tutorialspoint.com
    Accept-Language: en-us

    body of the request (typically in JSON for RestAPIs)
    """

    def parse_http(self, message):
        request_line_regex = r"([A-Z]+) ([^\s]+)+ HTTP\/[0-9]+.[0-9]+"
        header_regex = r"([0-9A-z-]+)\:[\s]*([^\n]+)"

        lines = message.split("\n")
        request_line = lines.pop(0)
        if m := re.search(request_line_regex, request_line):
            self.method = m.group(1)
            uri = m.group(2)
            [self.route, *params] = uri.split("?")
            if len(params) > 0:
                assignments = "".join(params).split("&")
                for assignment in assignments:
                    [key, value] = assignment.split("=")
                    self.query_params[key] = value
        else:
            raise HTTPException(status_code=401, detail="Bad Request")

        header = lines.pop(0)
        while len(lines) > 0 and (m := re.search(header_regex, header)):
            key = m.group(1)
            value = m.group(2)
            self.headers[key] = value
            header = lines.pop(0)

        self.body = "\n".join(lines).strip()
        try:
            if self.body:
                self.form_params = json.loads(self.body)
        except JSONDecodeError:
            raise HTTPException(status_code=401, detail="Bad Request")
