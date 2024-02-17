import json
import os


class Tournament:
    """This class contains information of a tournament, creates Tournament instances, loads and saves"""
    def __init__(self, name=None, start_date=None, end_date=None, venue=None, number_of_rounds=None,
                 current_round=None, is_complete=False, registered_players=None,
                 is_finished=None, rounds=None):

        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.venue = venue
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.is_completed = is_complete
        self.registered_players = registered_players
        self.is_finished = is_finished
        self.rounds = rounds

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
        print("----------------------------------------------------------------")
        print("        -- CREATING A NEW TOURNAMENT --")
        name = input("Enter the tournament name: ")
        start_date = input("Enter the tournament start date (DD-MM-YYYY): ")
        end_date = input("Enter the tournament end date (DD-MM-YYYY): ")
        venue = input("Enter the tournament's venue: ")
        number_of_rounds_input = input("Enter the number of rounds: ")
        number_of_rounds = int(number_of_rounds_input)
        current_round = 1
        is_complete = False
        registered_players = []
        is_finished = False
        rounds = []
        tournament = cls(name, start_date, end_date, venue, number_of_rounds, current_round, is_complete,
                         registered_players, is_finished, rounds)
        tournament.save()

    def save(self, filename=None):
        """This function serializes the Tournament information to the JSON file"""
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

            print(f"\nTournament data has been saved to {filename}")

    @classmethod
    def load_tournament(cls, filename):
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
                is_complete=data["completed"],
                registered_players=data["players"],
                is_finished=data.get("finished", "false"),
                rounds=data["rounds"],
            )
        except KeyError:
            print("ERROR: missing key in tournament data")
            return None
