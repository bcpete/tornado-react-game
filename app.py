from tornado import ioloop, web, websocket
import json

games = []

class EchoWebSocket(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    
    def open(self):
        print('websocket opened')

    def on_message(self, message):
        self.write_message('you said: ' + message)

    def on_close(self):
        print('websocket closed')

def make_app():
    return web.Application([
        (r"/ws", EchoWebSocket),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(3000)
    print('server started on port 3000')
    ioloop.IOLoop.current().start()
