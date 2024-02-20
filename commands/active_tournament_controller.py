import os
import json

from models.matches import Matches
from screens.tournaments.active_tournaments_view import ActiveTournamentView

DATA_TOURNAMENTS_FOLDER = "data/tournaments"


class ActiveTournamentController:

    def __init__(self, tournament):
        self.tournament = tournament

        # Method prints the information of current loaded tournament
    @classmethod
    def view_tournament_information(cls, tournament):
        print("Tournament View")
        print(f"Name: {tournament.name}")
        print(f"Start Date: {tournament.start_date}")
        print(f"End Date: {tournament.end_date}")
        print(f"Venue: {tournament.venue}")
        print(f"Number of Rounds: {tournament.number_of_rounds}")
        print(f"Current Round: {tournament.current_round}")
        print(f"Completed: {tournament.is_complete}")
        print(f"Players: {tournament.registered_players}")
        print(f"Finished: {tournament.is_finished}")
        print(f"Rounds: {tournament.rounds}")

    @staticmethod
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

    @staticmethod
    def manage_active_tournaments():
        while True:
            active_tournaments = ActiveTournamentController.get_active_tournaments(DATA_TOURNAMENTS_FOLDER)
            ActiveTournamentView.display_active_tournaments(active_tournaments)

            print("\nOptions:")
            print("Select a tournament number to view/modify or Enter 'X' to go back to the main menu")

            user_choice = input("Enter your choice: ")

            if user_choice.lower() == "x":
                break

            if user_choice.isdigit():
                tournament_number = int(user_choice)
                if tournament_number >= 1 and tournament_number <= len(active_tournaments):
                    selected_tournament = active_tournaments[tournament_number - 1]
                    ActiveTournamentController.modify_selected_tournament(selected_tournament)
                else:
                    print("Invalid tournament number. Please enter a valid number.")
            else:
                print("Invalid choice. Please enter a valid number or 'X'.")

    @staticmethod
    def modify_selected_tournament(selected_tournament):
        print("---------------------------------------------------------------------")
        print(f"VIEWING/MODIFYING: {selected_tournament}")
        print("\nCurrent Tournament Information:\n")
        ActiveTournamentController.view_tournament_information(selected_tournament[0])

        while True:
            print("\nTournament Options:")
            print("1. Modify tournament details")
            print("2. Add players to the tournament")
            print("3. Remove players from the tournament")
            print("4. Go back to the Active Tournaments List")

            user_choice = input("Enter your choice: ")

            if user_choice == "1":
                pass
            elif user_choice == "2":
                pass
            elif user_choice == "3":
                pass
            elif user_choice == "4":
                break  # Break the loop and go back to the main menu
            else:
                print("Invalid choice. Please enter a valid option.")
