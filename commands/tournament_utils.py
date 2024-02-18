import json
import os
from operator import itemgetter


def get_active_tournaments(folder_path):
    """This function retrieves all the active tournaments that are in the data/tournaments folder to
    display in descending order by date"""
    active_tournaments = []

    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".json"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path) as file:
                    data = json.load(file)
                    if not data.get("finished", False):
                        start_date = data["dates"]["from"]
                        active_tournaments.append((file_name, start_date))

    return active_tournaments


def display_active_tournaments(active_tournaments):
    if len(active_tournaments) >= 1:
        active_tournaments.sort(key=itemgetter(1))
        print("\n--------------------------------------------------------------------------")
        print("                  -- ACTIVE TOURNAMENT(s) --\n")
        for i, (file_name, start_date) in enumerate(active_tournaments, start=1):
            print(f"{i}. {file_name} - Start Date: {start_date}")
