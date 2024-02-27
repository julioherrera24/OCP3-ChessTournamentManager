import os
import json

# from models.matches import Matches
from models.tournament import Tournament
from screens.tournaments.completed_tournaments_view import CompletedTournamentView

# GLOBAL/CONSTANT VARIABLES
DATA_TOURNAMENTS_FOLDER = "data/tournaments"
DATA_CLUBS_FOLDER = "data/clubs"


class CompletedTournamentController:

    def __init__(self, tournament):
        """Constructor initializes objects of this class with specific tournament parameter"""
        self.tournament = tournament

    # A static method belongs to the class rather than the instance of the class.
    # It can be called on the class itself, without creating an instance.
    @staticmethod
    def view_tournament_information(tournament):
        # this method calls the view method that displays the tournament information
        CompletedTournamentView.display_tournament_information(tournament)

    @staticmethod
    def get_completed_tournaments(folder_path):
        """This function retrieves all the completed tournaments that are in the
        data/tournaments folder to display in descending order by end date"""

        # empty list that will hold all completed tournaments
        completed_tournaments = []

        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".json"):
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path) as file:
                        data = json.load(file)
                        # retrieve all tournaments that are finished and completed
                        if data.get("finished", True) and data.get("completed", True):
                            end_date = data["dates"]["to"]
                            completed_tournaments.append((file_name, end_date))

        return completed_tournaments

    @staticmethod
    def manage_completed_tournaments():
        """This method will allow the user to view completed tournament information and generate a report"""
        while True:
            # display all completed tournaments in descending order by end date
            completed_tournaments = CompletedTournamentController.get_completed_tournaments(DATA_TOURNAMENTS_FOLDER)
            completed_tournaments = CompletedTournamentView.display_completed_tournaments(completed_tournaments)

            # gets user input of which tournament they selected
            user_choice = CompletedTournamentView.get_tournament_choice()

            if user_choice.lower() == "x":
                break
            # gets the tournament user selected and file path to use as a parameter
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
    def view_selected_tournament(selected_tournament_file_path):
        """ this function will give the ability to select generate a report for tournament"""
        print("-" * 74)
        print(f"VIEWING: {selected_tournament_file_path}")

        # load the tournament and create a tournament object
        tournament = Tournament.load_tournament(selected_tournament_file_path)

        # displays the information of the selected tournament
        CompletedTournamentController.view_tournament_information(tournament)

        while True:
            # displays the options and gets the user selection
            inner_choice = CompletedTournamentView.completed_tournament_options_choice()

            if inner_choice == "1":
                CompletedTournamentController.generate_report(tournament)  # generates a report of tourney
            elif inner_choice == "2":
                break  # return to Completed Tournaments menu
            else:
                print("Invalid choice. Please enter a valid number option.")

    @staticmethod
    def generate_report(tournament):
        # DEBUG: loaded_tournament = Tournament.load_tournament(tournament)
        """This method displays the report"""
        CompletedTournamentView.display_report(tournament)
