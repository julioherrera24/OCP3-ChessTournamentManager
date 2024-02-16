class Matches:
    """Matches model
        All matches are associated with a round.
        All matches belong to a specific tournament

        Attributes:
        tournament_id (int): Unique id of the specific tournament.
        round_id (int): Unique id of the parent round.
        match_id (int):  Unique id of this match.
        winner (int): point value for winner/loser/draw.
        player_1 (Player): Arbitrary first player.
        player_2 (Player): Arbitrary second player.
    """

    # constructor for Matches
    def __init__(self, tournament_id, round_id, match_id, winner, players: tuple):

        self.tournament_id = tournament_id
        self.round_id = round_id
        self.match_id = match_id
        self.winner = winner

        # players(tuple[Player]): The two participating players in the match.
        self.player_1 = players[0]
        self.player_2 = players[1]

    def __str__(self):
        stdout_content = "    - {f_name_1} {l_name_1} vs {f_name_2} {l_name_2} \n".format(
            f_name_1=self.player_1.first_name,
            l_name_1=self.player_1.last_name,
            f_name_2=self.player_2.first_name,
            l_name_2=self.player_2.last_name,
        )
        stdout_content += "    Winner : {winner}\n".format(winner=self.winner)
        stdout_content += "    id : {id}\n".format(id=self.match_id)

        return stdout_content
