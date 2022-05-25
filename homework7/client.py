import socket
import json


class SocketClient:
    def __init__(self, host, port):
        self.host: str = host
        self.port: int = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(False)

    def make_request(self, params, method="GET", data=None, client_timeout=2, data_amount=4096, shutdown=False) -> tuple:
        self.client.settimeout(client_timeout)
        self.client.connect_ex((self.host, self.port))
        if data is None:
            request = f'{method} {params} HTTP/1.1\r\nHost:{self.host}\r\nConnection: close\r\n\r\n'
        else:
            data = json.dumps(data)
            content_length = len(str(data))
            request = f'{method} {params} HTTP/1.1\r\nHost:{self.host}\r\nContent-Type: application/json\r\nContent' \
                      f'-Length: {content_length}\r\n\r\n{data} '
        try:
            self.client.sendall(request.encode())
        except socket.timeout:
            if shutdown:
                self.client.close()
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                return 200, "Server is down"
            raise Exception("Response timeout")

        raw_headers, data = self.client.recv(data_amount).split(b"\r\n\r\n")

        raw_headers = raw_headers.decode().split()
        content_length = int(raw_headers[raw_headers.index('Content-Length:') + 1])
        status_code = int(raw_headers[raw_headers.index('HTTP/1.1') + 1])

        i = 0
        while len(data.decode()) < content_length:
            i += 1
            data += self.client.recv(data_amount)
            if i == 10:
                raise Exception("Something is broken...")

        self.client.close()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        return status_code, raw_headers, data.decode().strip().strip('"')
