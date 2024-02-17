import random


class Matches:
    """Matches model
        All matches are associated with a round.
        All matches belong to a specific tournament

        Attributes:
        players = players in the match
        winner = winner of the match
        is_completed = boolean whether match is completed or not
        points = contains the amount of points a player has
        tournament = the tournament the match is associated to
    """

    # constructor of Matches
    def __init__(self, tournament, players=None, winner=None, is_completed=None, points=None):

        self.players = players
        self.winner = winner
        self.is_completed = is_completed
        self.points = points
        self.tournament = tournament

    def create_pairing(self):
        """This function is responsible for creating the matchings for the matches
        For the first round we match randomly if there are an even amount of players
        For the following rounds, we calculate the points and create the matchings based on points"""
        if self.tournament.current_round == 1:
            return self.pair_randomly()
        else:
            self.calculate_points()
            return self.pair_based_on_points()

    def pair_randomly(self):
        """We create random pairings for the first round from the list of registered players"""
        players = self.tournament.registered_players[:]
        if len(players) % 2 != 0:
            print("Failed to make pairings. Cannot pair odd number of players.")
            print("Add another player to the tournament.")
            return

        random.shuffle(players)
        matches = []
        for i in range(0, len(players), 2):
            if i + 1 < len(players):
                matches.append((players[i], players[i + 1]))
        return matches

    def pair_based_on_points(self):
        """We will create the following match pairings based on points. We first sort the players based on points
        and then create pairings from the top to bottom"""
        sort_players = sorted(self.points.keys(), key=lambda player: self.points[player], reverse=True)
        matches = []
        while len(sort_players) >= 2:
            player1 = sort_players.pop(0)
            player2 = sort_players.pop(0)
            matches.append((player1, player2))
        return matches

    def calculate_points(self):
        """we add 0.5 points for the players in a match if it ended up as a draw
        we add 1 player to the player who was the winner of the match"""
        for round_data in self.tournament.rounds:
            winner = round_data.get("winner")
            if winner is None:
                players = round_data.get("players")
                if players:
                    for player in players:
                        self.points[player] += 0.5
            else:
                self.points[winner] += 1
