import os
import json

# from models.matches import Matches
from models.tournament import Tournament
from screens.tournaments.completed_tournaments_view import CompletedTournamentView

DATA_TOURNAMENTS_FOLDER = "data/tournaments"
DATA_CLUBS_FOLDER = "data/clubs"


class CompletedTournamentController:

    def __init__(self, tournament):
        self.tournament = tournament

    @staticmethod
    def view_tournament_information(tournament):
        CompletedTournamentView.display_tournament_information(tournament)

    @staticmethod
    def get_completed_tournaments(folder_path):
        """This function retrieves all the active tournaments that are in the
        data/tournaments folder to display in descending order by date"""
        completed_tournaments = []

        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".json"):
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path) as file:
                        data = json.load(file)
                        if data.get("finished", True) and data.get("completed", True):
                            end_date = data["dates"]["to"]
                            completed_tournaments.append((file_name, end_date))

        return completed_tournaments

    @staticmethod
    def manage_completed_tournaments():
        while True:
            completed_tournaments = CompletedTournamentController.get_completed_tournaments(DATA_TOURNAMENTS_FOLDER)
            completed_tournaments = CompletedTournamentView.display_completed_tournaments(completed_tournaments)

            user_choice = CompletedTournamentView.get_tournament_choice()

            if user_choice.lower() == "x":
                break

            if user_choice.isdigit():
                tournament_number = int(user_choice)
                if 1 <= tournament_number <= len(completed_tournaments):
                    selected_tournament = completed_tournaments[tournament_number - 1][0]
                    selected_tournament_file_path = os.path.join(DATA_TOURNAMENTS_FOLDER, selected_tournament)
                    # print(f"Selected tournament: {selected_tournament}")
                    # print(f"Selected tournament file path: {selected_tournament_file_path}")
                    CompletedTournamentController.view_selected_tournament(selected_tournament_file_path)

                else:
                    print("Invalid tournament number. Please enter a valid number.")
            else:
                print("Invalid choice. Please enter a valid number or 'X'.")

    @staticmethod
    def view_selected_tournament(selected_tournament):
        """ this function will give the ability to modify a tournament"""
        print("-" * 74)
        print(f"VIEWING: {selected_tournament}")

        # load the tournament and create a tournament object
        tournament = Tournament.load_tournament(selected_tournament)

        CompletedTournamentController.view_tournament_information(tournament)

        while True:
            inner_choice = CompletedTournamentView.completed_tournament_options_choice()

            if inner_choice == "1":
                CompletedTournamentController.generate_report(tournament)
            elif inner_choice == "2":
                break
            else:
                print("Invalid choice. Please enter a valid number option.")

    @staticmethod
    def generate_report(tournament):
        # loaded_tournament = Tournament.load_tournament(tournament)
        CompletedTournamentView.display_report(tournament)
