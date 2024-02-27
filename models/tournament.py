import json
import os

from datetime import datetime


class Tournament:
    """This class contains information of a tournament, creates Tournament instances,
    loads, saves tournament instances as well"""
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

    @classmethod
    def create_tournament(cls):
        """This method creates a new tournament with user input and calls the save function
         to save the information to a JSON file inside the data/tournaments folder"""
        print("-" * 74)
        print(f"{' ' * 20}-- CREATING A NEW TOURNAMENT --")

        # set the name of the tournament instance
        name = input("Enter the tournament name: ")

        # Validate user gives us the correct start date format
        while True:
            start_date_input = input("Enter the tournament start date (DD-MM-YYYY): ")
            try:
                start_date_date = datetime.strptime(start_date_input, "%d-%m-%Y").date()
                start_date = start_date_date.strftime("%d-%m-%Y")
                break  # breaks loop if the input is correctly formatted
            except ValueError:
                print("Invalid date format. Enter date as DD-MM-YYYY.")

        # validate user gives us the correct end date format
        while True:
            end_date_input = input("Enter the tournament end date (DD-MM-YYYY): ")
            try:
                end_date_date = datetime.strptime(end_date_input, "%d-%m-%Y").date()
                end_date = end_date_date.strftime("%d-%m-%Y")
                break   # breaks loop if correct format
            except ValueError:
                print("Invalid date format. Enter date as DD-MM-YYYY")

        # sets the venue of the tournament, some venues may have numbers or symbols in their name
        venue = input("Enter the tournament's venue: ")

        # Validate and get the number of rounds
        while True:
            number_of_rounds_input = input("Enter the number of rounds: ")
            if number_of_rounds_input.isdigit():
                number_of_rounds = int(number_of_rounds_input)
                break  # Break the loop if the input is a valid integer
            else:
                print("Invalid input. Please enter a valid number.")

        # initial values of attributes
        current_round = 1
        is_completed = False
        registered_players = []
        is_finished = False
        rounds = []
        tournament = cls(name, start_date, end_date, venue, number_of_rounds, current_round, is_completed,
                         registered_players, is_finished, rounds)

        # save tournament instance
        tournament.save()

        print("Tournament is now active. You can now access it in the 'View/Manage All Active Tournaments Screen'")
        print("Returning to Main Menu...")

    def save(self, filename=None):
        """This function serializes the Tournament information to the JSON file"""
        # if no directory of data/tournaments exists then we make one
        if not os.path.exists("data/tournaments"):
            os.makedirs("data/tournaments")

        # set the name of file as tournament name if filename is None
        if filename is None:
            if self.name is not None:
                filename = f"data/tournaments/{self.name.replace(' ', '_')}.json"
            else:
                print("No tournament file to save.")
                return
        else:
            filename += f"data/tournaments/{filename}.json"

        # save the information structured for easy extraction, replicates the example tournament instance
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
                    "rounds": self.rounds,
                    "points": self.points
                }, fp, indent=4)

            print(f"\nTournament data has been saved to {filename}.")

    @classmethod
    def load_tournament(cls, filename):
        """This method loads the information of a tournament instance from the JSON file."""

        # if no tournament file exists, return print statement
        if not os.path.exists(filename):
            print("No tournament was found.")
            return None

        # load information from file
        with open(filename) as file:
            data = json.load(file)

        try:
            tournament = cls(
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

            # Load points if available in the data
            tournament.points = data.get("points", {})

            return tournament

        except KeyError:
            print("ERROR: missing key in tournament data")
            return None

    def add_players(self, players):
        """This method adds players to the tournament. We use this method when registering
        players to a tournament. This method also initializes a registered players points to 0."""
        if not self.is_finished:
            self.registered_players.extend(players)
            for player in players:
                self.points[player["chess_id"]] = 0.0
            print(f"Players added to the tournament: {[player['name'] for player in players]}")
        else:
            print("Cannot add players to a finished tournament.")

    def update_points(self, players, points):
        """This method updates the points for the specified players in the tournament."""
        for player in players:
            # Use get method to safely retrieve the value associated with the player's key
            current_points = self.points.get(player, 0.0)
            # Update points for the player based on result of the match from "enter_results" method in controller
            self.points[player] = current_points + points
