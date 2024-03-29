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

    @staticmethod
    def pair_randomly(tournament):
        """We create random pairings for the first round from the list of registered players"""
        if tournament.current_round == 1:
            players = tournament.registered_players
            random.shuffle(players)

            matches = []
            for i in range(0, len(players), 2):
                if i + 1 < len(players):
                    matches.append({
                        "players": [players[i]["chess_id"], players[i + 1]["chess_id"]],
                        "completed": False,
                        "winner": None
                    })

            round_data_list = []

            for match in matches:
                # Extract player chess IDs
                player1 = match["players"][0]
                player2 = match["players"][1]

                # Create a dictionary for each pair with relevant information
                round_data = {
                    "players": [player1, player2],
                    "completed": False,
                    "winner": None
                }
                round_data_list.append(round_data)

            # Append the individual round dictionaries to the rounds list
            tournament.rounds.extend(round_data_list)

            # print(f"Round Data: {round_data_list}")
            # print(f"Updated Tournament Rounds: {self.tournament.rounds}")

            # self.tournament.save()
            return matches

    @staticmethod
    def pair_based_on_points(tournament):
        """We will create the following match pairings based on points. We first sort the players based on points
        and then create pairings from the top to bottom"""
        # print("Current Tournament Points:", tournament.points)

        sort_players = sorted(tournament.points.keys(), key=lambda player: tournament.points[player], reverse=True)

        # print("Sorted Players:", sort_players)

        matches = []
        while len(sort_players) >= 2:
            player1 = sort_players.pop(0)
            player2 = sort_players.pop(0)
            matches.append({
                "players": [player1, player2],
                "completed": False,
                "winner": None
            })

        round_data_list = []

        for match in matches:
            # Extract player chess IDs
            player1 = match["players"][0]
            player2 = match["players"][1]

            # Create a dictionary for each pair with relevant information
            round_data = {
                "players": [player1, player2],
                "completed": False,
                "winner": None
            }
            round_data_list.append(round_data)

        # Append the individual round dictionaries to the rounds list
        tournament.rounds.extend(round_data_list)

        # print(f"Round Data: {round_data_list}")
        # print(f"Updated Tournament Rounds: {self.tournament.rounds}")

        # self.tournament.save()
        return matches
