import json
from pathlib import Path

from .tournament import Tournament


class TournamentManager:
    """This class handles the proper creation of Tournament files and adds them to the data folder"""
    def __init__(self, data_folder="data/tournaments"):
        data_directory = Path(data_folder)
        self.data_folder = data_directory
        self.tournaments = []
        for filepath in data_directory.iterdir():
            if filepath.is_file() and filepath.suffix == ".json":
                try:
                    self.tournaments.append(Tournament(filepath))
                except json.JSONDecodeError:
                    print(filepath, "is an invalid JSON file.")

    def create(self, name):
        filepath = self.data_folder / (name.replace(" ", "") + ".json")
        tournament = Tournament(name=name, filepath=filepath)
        tournament.save()

        self.tournaments.append(tournament)
        return tournament
