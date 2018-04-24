from tornado import ioloop, web, websocket
import json
games = {}


class EchoWebSocket(websocket.WebSocketHandler):

    def initialize(self, *args, **kwargs):
        self.game_id = None
        super().initialize(*args, **kwargs)

    def check_origin(self, origin):
        return True
    
    def open(self):
        self.send_message(type="open", message="Connected to game server.")

    def on_message(self, message):
        data = json.loads(message)
        print(message)
        type = data.get("type", "")
        
        if type == "new-game":
            self.game_id = 1
            games[self.game_id] = {
                'player_1' : self
            }
            self.send_message(type='waiting', game_id=self.game_id)
        
        elif type == "join_game":
            game_id = int(data.get('game_id'))
            game = games.get(game_id)
            if game.get('player_2') is None:
                self.game_id = game_id
                game['player_2'] = self
                self.send_message(type="joined_game", game_id=self.game_id)
                game.get('player_1').send_message(type="joined_game", message="player 2 joined!")
            else:
                self.send_message(type="error", message="invalid game id")


    def on_close(self):
        print('websocket closed')

    def send_message(self, type, **data):
        message = {
            "type" : type,
            "data" : data
        }
        self.write_message(json.dumps(message))

def make_app():
    return web.Application([
        (r"/ws", EchoWebSocket),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(3000)
    print('server started on port 3000')
    ioloop.IOLoop.current().start()
