import json
import os
from operator import itemgetter
from datetime import datetime


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
    """This function displays the active tournaments found from earliest to oldest based on start date"""
    if len(active_tournaments) >= 1:
        # list to hold all tournament name and start_date as date object to sort
        active_tournaments_dates = []

        # iterate through active_tournaments to convert string date to object date
        for file_name, start_date in active_tournaments:
            date_obj = datetime.strptime(start_date, "%d-%m-%Y").date()
            active_tournaments_dates.append((file_name, date_obj))

        # sort dates from earliest to oldest
        active_tournaments_dates.sort(key=itemgetter(1), reverse=True)

        # print sorted active tournaments with string dates
        print("\n--------------------------------------------------------------------------")
        print("                  -- ACTIVE TOURNAMENT(s) --\n")

        for i, (file_name, start_date) in enumerate(active_tournaments_dates, start=1):
            print(f"{i}. {file_name} - Start Date: {start_date.strftime('%d-%m-%Y')}")
