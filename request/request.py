from urllib.parse import parse_qs


class Request:

    def __init__(self, file) -> None:

        self.file = file
        self.method = ''
        self.url = ''
        self.protocol = ''

        self.numbers = []

        self.headers = {}
        self.body = None

        self.parse_request_line()
        self.parse_headers()
        self.parse_body()
        self.parse_post_request()

    def parse_request_line(self) -> None:
        request_line = self.read_line()
        self.method, self.url, self.protocol = request_line.split(' ')
        if self.protocol != 'HTTP/1.1':
            raise ValueError('Wrong protocol')

    def parse_headers(self) -> None:
        while True:
            header = self.read_line()

            if header == '':
                break

            header_name, header_value = header.split(': ')
            self.headers[header_name] = header_value

    def parse_body(self) -> None:
        if 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
            self.body = self.file.read(content_length)

    def parse_post_request(self) -> None:
        if self.body:
            numbers = parse_qs(self.body.decode())
            if 'numbers' in numbers:
                self.numbers = numbers['numbers'][0].split()
            else:
                self.numbers = []

    def read_line(self) -> str:
        return self.file.readline().decode().strip()
