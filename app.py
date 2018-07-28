from tornado import ioloop, web, websocket
import json
from gamemaster import GameMaster
gamemaster = GameMaster()
connections = []

class GameWebSocket(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True
    
    def open(self):
        print('socket opened')
        connections.append(self)
        self.send_open_games()

    def on_message(self, message):
        data = json.loads(message)
        print(message)
        type = data.get("type", "")
        
        if type == "new-game":
            game_id = gamemaster.create_game(self)
            self.send_message(type='new-game', game_id=game_id)
            self.send_open_games()
        
        elif type == "join_game":
            game_id = data.get('game_id')
            game_to_join = gamemaster.join_game(game_id, self)
            if game_to_join:
                self.broadcast_message(type="joined_game", game_id=game_to_join, message="Player has joined game #{}".format(game_id))
            else:
                self.send_message(type="error", message="invalid game id")

        elif type == "make_move":
            game_id = data.get('game_id')
            move = int(data.get('move'))
            game = gamemaster.get_game(game_id)
            if game.get('player_1') == self:
                self.broadcast_message(type="move", move=move, player="player_1", game_id=game_id)
            else: 
                self.broadcast_message(type="move", move=move, player="player_2", game_id=game_id)


    def on_close(self):
        print('websocket closed')

    def send_message(self, type, **data):
        message = {
            "type" : type,
            "data" : data
        }
        self.write_message(json.dumps(message))

    def broadcast_message(self, type, **data):
        opponent = gamemaster.get_opponent(data['game_id'], self)
        opponent.send_message(type, **data)
        self.send_message(type, **data)

    def send_open_games(self):
        open_games = []
        for game in gamemaster.games:
            open_game = gamemaster.get_game(game)
            if open_game.get('player_2') == None:
                open_games.append(game)
        for connection in connections:
            connection.send_message(type='open-games', games=open_games)

def make_app():
    return web.Application([
        (r"/ws", GameWebSocket),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(3000)
    print('server started on port 3000')
    ioloop.IOLoop.current().start()
