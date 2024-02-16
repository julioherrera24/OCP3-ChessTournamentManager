class Round:
    """Round model
        All rounds have matches associated with them.
        Rounds belong to a specific tournament.

        Attributes:
        num_round (int): number of round in tournament.
        tournament_id (int): Unique id of the specific tournament.
        id_num (int): Unique id of this current round.
        matches (dict): All matches associated with this round.
    """

    # constructor of Round
    def __init__(self, num_round, tournament_id, id_num):

        self.num_round = num_round
        self.tournament_id = tournament_id
        self.id_num = id_num

        self.matches = {}

    def __str__(self):
        round_content = "- Round Number: {num}\n".format(num=self.num_round)

        round_content += " - Matches -\n"

        for started_match in self.matches:
            round_content += started_match.__str__()

        return round_content
