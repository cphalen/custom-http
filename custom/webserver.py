import socket
import threading
from custom.request import Request
from custom.response import Response
from custom.exception import HTTPException
import inspect
import json
import re


def thread_init(api):
    api.open_socket()
    api.await_request()


class CustomAPI:
    QUEUE_SIZE = 5
    MESSAGE_SIZE = 100000000
    HOSTNAME = "127.0.0.1"
    PORT = 8000
    TERMINATE_STRING = "\r\n\r\n"

    def __init__(self):
        self.routes = {
            "GET": {},
            "POST": {}
            # you would add the other HTTP methods here
        }
        self.thread = threading.Thread(target=thread_init, args=(self,))
        self.thread.start()
        self.debug = True
        print(f"CustomAPI listing on {self.HOSTNAME}:{self.PORT}")

    """
    open server socket on PORT which will listen for connections
    """

    def open_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOSTNAME, self.PORT))
        self.server_socket.listen(self.QUEUE_SIZE)

    """
    main look where we await connections and handle connections as they come
    """

    def await_request(self):
        while True:
            client_socket, _ = self.server_socket.accept()
            response = self.handle_request(client_socket)
            client_socket.send(response.encode())
            client_socket.close()

    """
    A couple of steps here:
        1. Read HTTP request text
        2. Parse request text into request object (see request.py mostly regex)
        3. Find endpoint (by method and route) associated with request. If
           there is no associated endpoint, throw a 404 Not Found
        4. Call endpoint to get response body
        5. Create response object with body and status code (see response.py
           to see how this is actually formatted into HTTP response message)
    """

    def handle_request(self, client_socket):
        try:
            message = self.read_message(client_socket)
            if self.debug:
                print("------------(HTTP request start)-------------")
                print(message)
                print("------------(HTTP request stop)--------------")
                print("\n")
            request = Request(message)
            endpoint = self.routes.get(request.method, {}).get(request.route, None)
            if not endpoint:
                raise HTTPException(status_code=404, detail="Not Found")
            result = self.call_endpoint(endpoint, request)
            body = json.dumps(result, indent=4)
            response = Response("200 OK", body)
        except HTTPException as e:
            status = f"{e.status_code} {e.detail}"
            body = json.dumps({"detail": e.detail}, indent=4)
            response = Response(status, body)
        except Exception as e:
            # why would I want to do this?
            message = "500 Server Error"
            print(e)
            response = Response(message, message)

        return response.format_response()

    """
    format arguments to endpoint and call endpoint, return endpoint result
    """

    def call_endpoint(self, endpoint, request):
        kwargs = {}
        args = inspect.signature(endpoint).parameters.keys()
        for arg in args:
            if request.method == "GET":
                kwargs[arg] = request.query_params.get(arg, "")
            elif request.method == "POST":
                kwargs[arg] = request.form_params.get(arg, "")
        return endpoint(**kwargs)

    """
    read HTTP request from socket
    """

    def read_message(self, client_socket):
        chunks = []
        body = ""
        while True:
            data = client_socket.recv(self.MESSAGE_SIZE).decode()
            if self.TERMINATE_STRING in data:
                chunk, body = data.split(self.TERMINATE_STRING)
                chunks.append(chunk)
                break
            else:
                chunks.append(data)

        preamble = "".join(chunks)
        content_length_regex = r"Content-Length:[\s]*([0-9]+)"
        if m := re.search(content_length_regex, preamble):
            content_length = int(m.group(1))
            while len(body) < content_length:
                data = client_socket.recv(self.MESSAGE_SIZE).decode()
                body += data

        return f"{preamble}\r\n\r\n{body}"

    # method functions

    def get(self, path):
        def decorator(f):
            self.routes["GET"][path] = f

        return decorator

    def post(self, path):
        def decorator(f):
            self.routes["POST"][path] = f

        return decorator
