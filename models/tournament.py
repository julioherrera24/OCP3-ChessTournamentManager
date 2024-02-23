import json
import os

from datetime import datetime

from models.matches import Matches


class Tournament:
    """This class contains information of a tournament, creates Tournament instances, loads and saves"""
    def __init__(self, name=None, start_date=None, end_date=None, venue=None, number_of_rounds=None,
                 current_round=None, is_completed=False, registered_players=None,
                 is_finished=None, rounds=None):

        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.venue = venue
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.is_completed = is_completed
        self.registered_players = registered_players
        self.is_finished = is_finished
        self.rounds = rounds
        self.points = {}

    def __str__(self):
        tournament_content = "- Tournament name: {name}\n".format(name=self.name)
        tournament_content += "- Start Date: {start_date}\n".format(start_date=self.start_date)
        tournament_content += "- End Date: {end_date}\n".format(end_date=self.end_date)
        tournament_content += "- Venue: {location}\n".format(location=self.venue)
        tournament_content += "- Total Number of rounds: {num}\n".format(num=self.number_of_rounds)
        tournament_content += "- Current Round: {curr}\n".format(curr=self.current_round)
        tournament_content += "- Completed?: {completed}\n".format(completed=self.is_completed)
        tournament_content += "- Players: {players}\n".format(players=self.registered_players)
        tournament_content += "- Finished?: {finished}\n".format(finished=self.is_finished)
        tournament_content += "- Rounds: {rounds}\n".format(rounds=self.rounds)

        return tournament_content

    @classmethod
    def create_tournament(cls):
        """This method creates a new tournament with user input and calls the save function
         to save the information to a JSON file"""
        print("--------------------------------------------------------------------------")
        print("        -- CREATING A NEW TOURNAMENT --")
        name = input("Enter the tournament name: ")

        # Validate user gives us the correct start date format
        while True:
            start_date_input = input("Enter the tournament start date (DD-MM-YYYY): ")
            try:
                start_date_date = datetime.strptime(start_date_input, "%d-%m-%Y").date()
                start_date = start_date_date.strftime("%d-%m-%Y")
                break  # breaks loop if the input is correctly formatted
            except ValueError:
                print("Invalid date format. Enter data as DD-MM-YYYY.")

        # validate user gives us the correct end date format
        while True:
            end_date_input = input("Enter the tournament end date (DD-MM-YYYY): ")
            try:
                end_date_date = datetime.strptime(end_date_input, "%d-%m-%Y").date()
                end_date = end_date_date.strftime("%d-%m-%Y")
                break   # breaks loop if correct format
            except ValueError:
                print("Invalid date format. Enter date as DD-MM-YYYY")

        venue = input("Enter the tournament's venue: ")

        # Validate and get the number of rounds
        while True:
            number_of_rounds_input = input("Enter the number of rounds: ")
            if number_of_rounds_input.isdigit():
                number_of_rounds = int(number_of_rounds_input)
                break  # Break the loop if the input is a valid integer
            else:
                print("Invalid input. Please enter a valid number.")

        current_round = 1
        is_completed = False
        registered_players = []
        is_finished = False
        rounds = []
        tournament = cls(name, start_date, end_date, venue, number_of_rounds, current_round, is_completed,
                         registered_players, is_finished, rounds)
        tournament.save()
        print("Tournament is now active. You can now access it in the 'View/Manage All Active Tournaments Screen")
        print("Returning to Main Menu...")

    def save(self, filename=None):
        """This function serializes the Tournament information to the JSON file"""
        # if not directory of data/tournaments exists then we make one
        if not os.path.exists("data/tournaments"):
            os.makedirs("data/tournaments")
        if filename is None:
            if self.name is not None:
                filename = f"data/tournaments/{self.name.replace(' ', '_')}.json"
            else:
                print("No tournament file to save.")
                return
        else:
            filename += f"data/tournaments/{filename}.json"

        with open(filename, "w") as fp:
            json.dump(
                {
                    "name": self.name,
                    "dates": {
                        "from": self.start_date,
                        "to": self.end_date
                    },
                    "venue": self.venue,
                    "number_of_rounds": self.number_of_rounds,
                    "current_round": self.current_round,
                    "completed": self.is_completed,
                    "players": self.registered_players,
                    "finished": self.is_finished,
                    "rounds": self.rounds
                }, fp, indent=4)

            print(f"\nTournament data has been saved to {filename}.")

    @classmethod
    def load_tournament(cls, filename):
        # print(f"Loading tournament from file: {filename}")
        if not os.path.exists(filename):
            print("No tournament was found.")
            return None

        with open(filename) as file:
            data = json.load(file)

        try:
            return cls(
                name=data["name"],
                start_date=data["dates"]["from"],
                end_date=data["dates"]["to"],
                venue=data["venue"],
                number_of_rounds=data["number_of_rounds"],
                current_round=data["current_round"],
                is_completed=data["completed"],
                registered_players=data["players"],
                is_finished=data.get("finished", "false"),
                rounds=data["rounds"],
            )
        except KeyError:
            print("ERROR: missing key in tournament data")
            return None

    def add_players(self, players):
        """Add players to the tournament."""
        if not self.is_finished:
            self.registered_players.extend(players)
            for player in players:
                self.points[player["chess_id"]] = 0.0
            print(f"Players added to the tournament: {[player['name'] for player in players]}")
        else:
            print("Cannot add players to a finished tournament.")

    def create_pairs(self, registered_players):
        """Create pairs for matches based on the tournament logic."""
        # Ensure the tournament has the correct number of players
        if len(registered_players) % 2 != 0:
            print("Failed to make pairings. Cannot pair an odd number of players.")
            print("Add another player to the tournament.")
            return

        matches = Matches(self)

        pairs = matches.create_pairing(registered_players)

        print("\nGenerated match pairs: ")
        for pair in pairs:
            player1_id = pair["players"][0]
            player2_id = pair["players"][1]
            print(f"-- {player1_id} vs. {player2_id} --")

    def update_points(self, players, points):
        """Update points for the specified players."""
        for player in players:
            self.points[player] += points
