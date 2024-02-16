import json
import os

class Tournament:
    """This class contains information of a tournament, creates Tournament instances, loads and saves
    and deletes them as well"""
    def __init__(self, filepath=None, name=None):

        self.name = name
        self.start_date = None
        self.end_date = None
        self.venue = None
        self.num_rounds = None
        self.current_round = None
        self.is_completed = None
        self.registered_players = []
        self.is_finished = None
        self.rounds = []
        self.filepath = filepath

        if filepath and not name:
            # Load data of tournament from JSON file
            with open(filepath) as fp:
                data = json.load(fp)
                self.name = data.get("name")
                dates = data.get("dates", {})
                self.start_date = dates.get("from")
                self.end_date = dates.get("to")
                self.venue = data.get("venue")
                self.num_rounds = data.get("number_of_rounds")
                self.current_round = data.get("current_round")
                self.is_completed = data.get("completed")
                self.registered_players = data.get("players", [])
                self.is_finished = data.get("finished")
                self.rounds = data.get("rounds", [])

        elif not filepath:
            # we did not have a file, so we are going to create it by running save method
            self.save()

    def __str__(self):
        tournament_content = "- Tournament name: {name}\n".format(name=self.name)
        tournament_content += "- Start Date: {start_date}\n".format(start_date=self.start_date)
        tournament_content += "- End Date: {end_date}\n".format(end_date=self.end_date)
        tournament_content += "- Venue: {location}\n".format(location=self.venue)
        tournament_content += "- Total Number of rounds: {num}\n".format(num=self.num_rounds)
        tournament_content += "- Current Round: {curr}\n".format(curr=self.current_round)
        tournament_content += "- Completed?: {completed}\n".format(completed=self.is_completed)
        tournament_content += "- Players: {players}\n".format(players=self.registered_players)
        tournament_content += "- Finished?: {finished}\n".format(finished=self.is_finished)
        tournament_content += "- Rounds: {rounds}\n".format(rounds=self.rounds)

        return tournament_content

    def save(self):
        """This function serializes the Tournament information to the JSON file"""
        with open(self.filepath, "w") as fp:
            json.dump(

            )
