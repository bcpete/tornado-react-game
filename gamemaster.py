class GameMaster(object):

    def __init__(self):
        self.games = {}
        self.game_id = 1
    
    def next_game_id(self):
        self.game_id +=1
        return self.game_id

    def get_game(self, game_id):
        game = self.games.get(game_id)
        return game

    def create_game(self, player_1):
        game_id = self.next_game_id()
        self.games[game_id] = {
            'player_1': player_1
        }
        return game_id

    def join_game(self, game_id, player_2):
        game = self.games.get(game_id)
        if game:
            if game.get('player_2') == None:
                game['player_2'] = player_2
                return game_id
        return None

    def get_opponent(self, game_id, player):
        game = self.games.get(game_id)
        print(game)
        if game.get('player_1') == player:
            return game.get('player_2')
        else:
            return game.get('player_1')

    def end_game(self, game_id):
        if game_id in self.games:
            del self.games[game_id]