import os
import json

from models.matches import Matches


class TournamentController:

    def __init__(self, tournament):
        self.tournament = tournament

        # Method prints the information of current loaded tournament
    def view_tournament(self):
        print("Tournament View")
        print(f"Name: {self.tournament.name}")
        print(f"Start Date: {self.tournament.start_date}")
        print(f"End Date: {self.tournament.end_date}")
        print(f"Venue: {self.tournament.venue}")
        print(f"Number of Rounds: {self.tournament.number_of_rounds}")
        print(f"Current Round: {self.tournament.current_round}")
        print(f"Completed: {self.tournament.is_complete}")
        print(f"Players: {self.tournament.registered_players}")
        print(f"Finished: {self.tournament.is_finished}")
        print(f"Rounds: {self.tournament.rounds}")

