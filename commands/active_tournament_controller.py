import os
import json

from models.matches import Matches
from models.tournament import Tournament
from screens.tournaments.active_tournaments_view import ActiveTournamentView

DATA_TOURNAMENTS_FOLDER = "data/tournaments"
DATA_CLUBS_FOLDER = "data/clubs"


class ActiveTournamentController:

    def __init__(self, tournament):
        self.tournament = tournament

        # Method prints the information of current loaded tournament

    @staticmethod
    def view_tournament_information(tournament):
        print(f"Name: {tournament.name}")
        print(f"Start Date: {tournament.start_date}")
        print(f"End Date: {tournament.end_date}")
        print(f"Venue: {tournament.venue}")
        print(f"Number of Rounds: {tournament.number_of_rounds}")
        print(f"Current Round: {tournament.current_round}")
        print(f"Completed: {tournament.is_completed}")
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
                        if not data.get("finished", False) and not data.get("completed", False):
                            start_date = data["dates"]["from"]
                            active_tournaments.append((file_name, start_date))

        return active_tournaments

    @staticmethod
    def manage_active_tournaments():
        while True:
            active_tournaments = ActiveTournamentController.get_active_tournaments(DATA_TOURNAMENTS_FOLDER)
            active_tournaments = ActiveTournamentView.display_active_tournaments(active_tournaments)

            print("\nOptions:")
            print("Select a tournament number to view/modify or Enter 'X' to go back to the main menu")

            user_choice = input("Enter your choice: ")

            if user_choice.lower() == "x":
                break

            if user_choice.isdigit():
                tournament_number = int(user_choice)
                if tournament_number >= 1 and tournament_number <= len(active_tournaments):
                    selected_tournament = active_tournaments[tournament_number - 1][0]
                    selected_tournament_file_path = os.path.join(DATA_TOURNAMENTS_FOLDER, selected_tournament)
                    # print(f"Selected tournament: {selected_tournament}")
                    # print(f"Selected tournament file path: {selected_tournament_file_path}")
                    ActiveTournamentController.modify_selected_tournament(selected_tournament_file_path)

                else:
                    print("Invalid tournament number. Please enter a valid number.")
            else:
                print("Invalid choice. Please enter a valid number or 'X'.")

    @staticmethod
    def modify_selected_tournament(selected_tournament):
        """ this function will give the ability to modify a tournament"""
        print("--------------------------------------------------------------------------")
        print(f"VIEWING/MODIFYING: {selected_tournament}")

        # load the tournament and create a tournament object
        tournament = Tournament.load_tournament(selected_tournament)

        print("\nCurrent Tournament Information:")
        ActiveTournamentController.view_tournament_information(tournament)

        while True:
            print("\n         -- ACTIVE TOURNAMENT OPTIONS --")
            print("1. Register a player for the currently selected tournament")
            print("2. Enter results of the match for the current round")
            print("3. Advance to the next round")
            print("4. Generate a tournament report")
            print("5. Return to the Active Tournaments List Menu")

            inner_choice = input("\nEnter your choice: ")

            if inner_choice == "1":
                ActiveTournamentController.register_players(tournament)
            elif inner_choice == "2":
                ActiveTournamentController.enter_results(tournament)
            elif inner_choice == "3":
                pass
            elif inner_choice == "4":
                pass
            elif inner_choice == "5":
                break  # Break the loop and go back to the main menu
            else:
                print("Invalid choice. Please enter a valid number option.")

    @staticmethod
    def register_players(tournament):
        """this function retrieves all the players in every club in order to register them for a tournament"""
        list_of_players = []
        club_files = []

        for file in os.listdir(DATA_CLUBS_FOLDER):
            if file.endswith(".json"):
                club_files.append(os.path.join(DATA_CLUBS_FOLDER, file))

        for file in club_files:
            with open(file) as filepath:
                data = json.load(filepath)
                players = data.get("players", [])
                list_of_players.extend(players)

        ActiveTournamentView.display_all_players(list_of_players)

        def search_by_name(player_name):
            matching_player_names = []
            for p in list_of_players:
                if player_name.lower() in p.get("name").lower():
                    matching_player_names.append(p)
            return matching_player_names

        def search_by_id(player_id):
            for p in list_of_players:
                if p.get("chess_id") == player_id:
                    return p
            return None

        selected_tournament_players = []
        while True:
            print("\n--------------------------------------------------------------------------")
            print("Type the number associated with the player you would like to add to the tournament or ")
            print("Type 'ID' to search for a player by Chess ID or ")
            print("Type 'Name' to search for a player by Name or ")
            print("Type 'X' to finish registering players and/or to return to Tournament options")

            option = input("\nYour choice is: ")

            if option.isdigit() and 1 <= int(option) <= len(list_of_players):
                selected_tournament_players.append(list_of_players[int(option) - 1])
                print(f"Added {list_of_players[int(option) - 1].get('name')} to the tournament.")

            elif option.lower() == 'id':
                chess_id = input("Enter Chess ID: ").strip()
                player = search_by_id(chess_id)
                if player:
                    selected_tournament_players.append(player)
                    print(f"Added {player.get('name')} to the tournament.")
                else:
                    print("No players match that Chess ID.")

            elif option.lower() == 'name':
                name = input("Enter the name of the player: ")
                matching_names = search_by_name(name)
                if matching_names:
                    # case where multiple players match the name
                    print("Players found:")
                    for i, player in enumerate(matching_names, 1):
                        print(f"{i}. {player.get('name')}")
                    selection = input("Select the player number to add: ")
                    if selection.isdigit() and 1 <= int(selection) <= len(matching_names):
                        selected_tournament_players.append(matching_names[int(selection) - 1])
                        print(f"Player {matching_names[int(selection) - 1].get('name')} added to the tournament.")
                    else:
                        print("Invalid selection.")
                else:
                    print("ERROR: No players match that name.")

            elif option.lower() == 'x':
                # Ensure the number of players is even before proceeding
                if len(selected_tournament_players) % 2 != 0:
                    print("ERROR: The number of selected players must be even. Please add another player.")
                else:
                    break

            else:
                print("ERROR: Select the correct Player number or the correct 'keyword' to add players.")

        tournament.add_players(selected_tournament_players)
        tournament.create_pairs(selected_tournament_players)
        tournament.save()
        print("First round matches have been set. Returning to Tournament Options screen...")

    @staticmethod
    def enter_results(tournament):
        print("--------------------------------------------------------------------------")
        print("                 -- ENTERING THE MATCH RESULTS --")

        print("\nCurrent matches in tournament round:")
        for i, match in enumerate(tournament.rounds, 1):
            player1, player2 = match['players']
            print(f"{i}. {player1} vs. {player2}")

        for match in tournament.rounds:
            # print(f"Processing round: {match}")
            print(f"\n * MATCH: {match['players'][0]} vs {match['players'][1]} *")
            print("-----------------------------------")

            if not match["completed"]:
                while True:
                    winner = input("\nEnter the Chess ID of the player who won this match (or 'draw' for a draw): ")
                    if winner.lower() == 'draw':
                        match['winner'] = None  # Mark the match as a draw
                        match['completed'] = True
                        print("Match ended as a DRAW, both players will receive 0.5 points.")
                        tournament.update_points(match['players'], 0.5)
                        break
                    elif winner in match["players"]:
                        match['winner'] = winner
                        match['completed'] = True
                        print(f"{winner} won this match, player will receive 1 point.")
                        tournament.update_points([winner], 1)
                        break
                    else:
                        print("Invalid input. Please enter a valid player ID.")
            if tournament.current_round == tournament.number_of_rounds:
                tournament.is_finished = True
                tournament.is_completed = True

        tournament.save()
        print("Updated Points:", tournament.points)
        print("Scores have been saved. Returning to Tournament Menu...")

