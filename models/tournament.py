class Tournament:
    """Tournament model:
        All tournaments have rounds associated with them.
        All rounds have matches associated with them.

        Attributes:
        name (str): name of tournament.
        venue (str): location of tournament.
        start_date (str): day tournament started.
        end_date (str): day tournament ended.
        is_completed (bool): whether tournament is completed or not
        registered_players (list): List of registered players.
        unique_id (int): Tournament's unique id.
        leaderboard (dict): Tournament's leaderboard.
        num_rounds (int): Number of rounds.
        current_round (int): current round of tournament
        all_rounds (dict): All rounds associated with this tournament.
    """

    # constructor of Tournament
    def __init__(self, name, venue, start_date, end_date, unique_id, registered_players: list,
                 leaderboard: dict, is_completed: bool, num_rounds=0, current_round=0):

        self.name = name
        self.venue = venue
        self.start_date = start_date
        self.end_date = end_date
        self.is_completed = is_completed
        self.registered_players = registered_players
        self.unique_id = unique_id
        self.leaderboard = leaderboard
        self.num_rounds = num_rounds
        self.current_round = current_round
        self.all_rounds = {}

    def __str__(self):
        tournament_content = "Tournament name: {name}\n".format(name=self.name)
        tournament_content += "- Venue: {location}\n".format(location=self.venue)
        tournament_content += "- Start Date: {start_date}\n".format(start_date=self.start_date)
        tournament_content += "- End Date: {end_date}\n".format(end_date=self.end_date)
        tournament_content += "- Total Number of rounds: {num}\n".format(num=self.num_rounds)
        tournament_content += "- Players: {players}\n".format(players=self.registered_players)
        tournament_content += "- Leaderboard: {leaderboard}\n".format(leaderboard=self.leaderboard)

        tournament_content += " - - Started rounds - -\n"

        for started_round in self.all_rounds:
            tournament_content += started_round.__str__()

        return tournament_content
