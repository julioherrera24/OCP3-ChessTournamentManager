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
        self.points = points if points is not None else {}
        self.tournament = tournament

    def create_pairing(self, players):
        """This function is responsible for creating the matchings for the matches
        For the first round we match randomly if there are an even amount of players
        For the following rounds, we calculate the points and create the matchings based on points"""
        if self.tournament.current_round == 1:
            matches = Matches.pair_randomly(players)
        else:
            self.calculate_points()
            matches = self.pair_based_on_points()

        # creates a list to store individual round dictionaries
        round_data_list = []

        for match in matches:
            # Extract player chess IDs
            player1 = match["players"][0]
            player2 = match["players"][1]

            # Create a dictionary for each pair with relevant information
            round_data = {
                "players": [
                    player1,
                    player2
                ],
                "completed": False,
                "winner": None
            }
            round_data_list.append(round_data)

        # Append the individual round dictionaries to the rounds list
        self.tournament.rounds.extend(round_data_list)

        # print(f"Round Data: {round_data_list}")
        # print(f"Updated Tournament Rounds: {self.tournament.rounds}")

        # self.tournament.save()
        return matches

    @staticmethod
    def pair_randomly(players):
        """We create random pairings for the first round from the list of registered players"""
        random.shuffle(players)
        matches = []
        for i in range(0, len(players), 2):
            if i + 1 < len(players):
                matches.append({
                    "players": [players[i]["chess_id"], players[i + 1]["chess_id"]],
                    "completed": False,
                    "winner": None
                })
        return matches

    def pair_based_on_points(self):
        """We will create the following match pairings based on points. We first sort the players based on points
        and then create pairings from the top to bottom"""
        sort_players = sorted(self.points.keys(), key=lambda player: self.points[player], reverse=True)
        matches = []
        while len(sort_players) >= 2:
            player1 = sort_players.pop(0)
            player2 = sort_players.pop(0)
            matches.append({
                "players": [player1, player2],
                "completed": False,
                "winner": None
            })
        return matches

    def calculate_points(self):
        """we add 0.5 points for the players in a match if it ended up as a draw
        we add 1 player to the player who was the winner of the match"""
        for round_data in self.tournament.rounds:
            winner = round_data.get("winner")
            if winner is None:
                players = round_data.get("players")
                if players:
                    for player_id in players:
                        self.points[player_id] += 0.5
            else:
                for player_id in round_data["players"]:
                    # Check if the player is player1 or player2 in the match
                    if player_id == winner:
                        self.points[player_id] += 1
                    else:
                        self.points[player_id] += 0

