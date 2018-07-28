import uuid

class GameMaster(object):

    def __init__(self):
        self.games = {}
        self.game_id = str(uuid.uuid4())

    def get_game(self, game_id):
        game = self.games.get(game_id)
        return game

    def create_game(self, player_1):
        game_id = str(uuid.uuid4())
        self.games[game_id] = {
            'player_1': player_1
        }
        return game_id

    def join_game(self, game_id, player_2):
        game = self.get_game(game_id)
        if game:
            if game.get('player_2') == None:
                game['player_2'] = player_2
                return game_id
        return None

    def get_opponent(self, game_id, player):
        game = self.get_game(game_id)
        print(game)
        if game.get('player_1') == player:
            return game['player_2']
        else:
            return game['player_1']

    def delete_game(self, game_id):
        if game_id in self.games:
            del self.games[game_id]