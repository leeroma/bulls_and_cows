from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler

from request.request import Request
from request.response import Response
from request import Status
from generate_numbers import generate_numbers
from bulls_and_cows import BullsAndCows


class NumbersConstant:
    RANDOM_NUMBERS = generate_numbers()


class MyTCPHandler(StreamRequestHandler):
    def handle(self):

        request = Request(self.rfile)
        response = Response(self.wfile)

        bulls_and_cows = BullsAndCows(NumbersConstant.RANDOM_NUMBERS)

        if '.css' in request.url:
            body = self.set_css(request, response)

        else:
            server_answer = self.parse_url(request.url)

            if '404' in server_answer:
                response.set_status = Status.NOT_FOUND

            if request.numbers:
                server_answer += self._prepare_numbers(request, bulls_and_cows)

            if bulls_and_cows.bulls == 4:
                server_answer += self._win_message()
                NumbersConstant.RANDOM_NUMBERS = generate_numbers()

            body = self._prepare_body(body=server_answer)
            self.set_html(response)

        response.add_header('Connection', 'close')
        response.set_body(body)
        response.send()

    @staticmethod
    def _prepare_body(**kwargs):
        template_path = 'static/index.html'
        with open(template_path, 'r') as template:
            body = template.read()
            body = body.format(**kwargs)

        return body

    @staticmethod
    def set_css(request: Request, response: Response):
        with open(request.url.lstrip('/')) as css:
            body = css.read()
            response.add_header('Content-Type', 'text/css')
            response.set_status(Status.OK)
        return body

    @staticmethod
    def set_html(response):
        response.add_header('Content-type', 'text/html')

    @staticmethod
    def parse_url(url):
        match url:
            case '/':
                return '</br><a href="/game">Game page</a><br/><a href="/rules">Rules</a>'

            case '/game':
                return ('<h1>Game page</h1><p>Guess 4 numbers. Enter them separated with spaces:</p>'
                        '<form method="POST" action=""><input type="text" name="numbers"/>'
                        '<input type="submit" value="Send" class="btn"/></form>')

            case '/rules':
                return ('<h1>Rules</h1><p>Your task is to guess four randomly generated numbers from 1 to 10</p>'
                        '<p>Type four numbers separated with spaces and click "send"</p>'
                        '<p>If you get a number and its position right - you get "bulls"</p>'
                        '<p>If you get a number right but different position - you get "cows"</p>'
                        '<p>Four bulls and you win!<p1></br><form method="POST" action="/">'
                        '<input type="submit" value="Return" class="btn"/></form>')

            case _:
                return '<h1>404 Not Found</h1>'

    @staticmethod
    def _prepare_numbers(request: Request, game: BullsAndCows) -> str:
        try:
            numbers = [int(num) for num in request.numbers]
            if len(numbers) != 4:
                raise ValueError
            game.guess_numbers(numbers)
            server_answer = f'<h1>Bulls: {game.bulls} Cows: {game.cows}</h1>'
            return server_answer
        except ValueError:
            return f'<h1>Incorrect input</h1>'

    @staticmethod
    def _win_message() -> str:
        server_answer = ('<h1>You won! Wanna play again?</h1><div class="btn-wrapper"><form method="POST" '
                         'action="/game"><input type="submit" value="Yes" class="btn"/>'
                         '</form><form method="POST" action="/"><input type="submit" value="No" class="btn"/>'
                         '</div></form>')
        return server_answer


class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    ...
