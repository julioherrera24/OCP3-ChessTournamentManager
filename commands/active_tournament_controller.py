import os
import json

from models.matches import Matches
from models.tournament import Tournament
from screens.tournaments.active_tournaments_view import ActiveTournamentView

# CONSTANT/GLOBAL VARIABLES
DATA_TOURNAMENTS_FOLDER = "data/tournaments"
DATA_CLUBS_FOLDER = "data/clubs"


class ActiveTournamentController:

    def __init__(self, tournament):
        """Constructor initializes objects of this class with specific tournament parameter"""
        self.tournament = tournament

    """A static method belongs to the class rather than the instance of the class."""
    """It can be called on the class itself, without creating an instance."""
    @staticmethod
    def view_tournament_information(tournament):
        # this method calls the view method that displays the tournament information
        ActiveTournamentView.display_tournament_information(tournament)

    @staticmethod
    def get_active_tournaments(folder_path):
        """This method retrieves all the tournaments that are active (complete, finished = False) in the
        data/tournaments folder to display in descending order by date"""

        # empty list that will hold the active tournaments
        active_tournaments = []

        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".json"):
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path) as file:
                        data = json.load(file)
                        # retrieve all tournaments that are not complete
                        if not data.get("finished", False) and not data.get("completed", False):
                            # retrieve the start date in order sort the list as the requirements want
                            start_date = data["dates"]["from"]
                            active_tournaments.append((file_name, start_date))

        return active_tournaments

    @staticmethod
    def manage_active_tournaments():
        """This method is used when the list of all the active tournaments are displayed to the user.
        The user can select which tournament they would like to modify/view"""
        while True:
            # retrieve and display all sorted active tournaments
            active_tournaments = ActiveTournamentController.get_active_tournaments(DATA_TOURNAMENTS_FOLDER)
            active_tournaments = ActiveTournamentView.display_active_tournaments(active_tournaments)

            # user selects a tournament based on their index on the list displayed
            user_choice = ActiveTournamentView.get_tournament_choice()

            if user_choice.lower() == "x":  # return to main menu
                break

            if user_choice.isdigit():
                tournament_number = int(user_choice)
                if 1 <= tournament_number <= len(active_tournaments):  # ensure user choice is a number from the list
                    # retrieve the tournament from the active tournaments and pass the file path to the modify method
                    selected_tournament = active_tournaments[tournament_number - 1][0]
                    selected_tournament_file_path = os.path.join(DATA_TOURNAMENTS_FOLDER, selected_tournament)
                    # print(f"Selected tournament: {selected_tournament}")
                    # print(f"Selected tournament file path: {selected_tournament_file_path}")
                    ActiveTournamentController.modify_selected_tournament(selected_tournament_file_path)
                else:
                    # user input a number that was not on the list
                    print(f"Invalid tournament number. Please enter a number from 1 - {len(active_tournaments)}.")
            else:
                # user entered non integer characters
                print("Invalid choice. Please enter a valid number or 'X' to go back to main menu.")

    @staticmethod
    def modify_selected_tournament(selected_tournament_file_path):
        """ this function will give the ability to modify a tournament. There are many different options
        that the user can select from, such as adding players, entering results from a round, advancing rounds
        and once a tournament is complete, get the report"""
        print("-" * 74)
        print(f"VIEWING/MODIFYING: {selected_tournament_file_path}")

        # load the tournament and create a tournament object instance
        tournament = Tournament.load_tournament(selected_tournament_file_path)

        # initially displays the information that the tournament contains
        ActiveTournamentController.view_tournament_information(tournament)

        while True:
            # gets the user choice and goes to method of what they want to do.
            # user should initially register players after tournament is created
            inner_choice = ActiveTournamentView.active_tournament_options_choice()

            if inner_choice == "1":
                ActiveTournamentController.register_players(tournament)
            elif inner_choice == "2":
                ActiveTournamentController.enter_results(tournament)
            elif inner_choice == "3":
                ActiveTournamentController.advance_to_next_round(tournament)
            elif inner_choice == "4":
                ActiveTournamentController.generate_report(tournament)
            elif inner_choice == "5":
                break  # Break the loop and go back to the Active Tournament List Menu
            else:
                print("Invalid choice. Please enter a valid number option (1 - 5).")

    @staticmethod
    def register_players(tournament):
        """this function retrieves all the players in every club in order to
            register them for a tournament and processes the user choice and entries to enter players
            into the tournament"""

        if tournament.is_completed:
            print("ERROR: The Tournament is completed. There are no more rounds.")
            return
        elif tournament.current_round > 1:
            print("ERROR: Tournament is already in progress. Cannot add more players.")
            return

        # empty lists that will be used to retrieve all players from all clubs
        list_of_players = []
        club_files = []

        # add all the club files to club_files
        for file in os.listdir(DATA_CLUBS_FOLDER):
            if file.endswith(".json"):
                club_files.append(os.path.join(DATA_CLUBS_FOLDER, file))

        # add all players in all the club_files to list_of_players list
        for file in club_files:
            with open(file) as filepath:
                data = json.load(filepath)
                players = data.get("players", [])
                list_of_players.extend(players)

        # calls the view method to display all the players with their index number
        ActiveTournamentView.display_all_players(list_of_players)

        def search_by_name(player_name):
            """this method returns that matching player names that the user searches for.
            User can enter a few characters and will return a list of players that match
            User will be able to choose from their index of the returned list"""
            matching_player_names = []
            for p in list_of_players:
                if player_name.lower() in p.get("name").lower():
                    matching_player_names.append(p)
            return matching_player_names

        def search_by_id(player_id):
            """this method returns the players whose chess_id matches from the list"""
            for p in list_of_players:
                if p.get("chess_id") == player_id:
                    return p
            return None

        # list that will hold all the registered players for the tournament
        selected_tournament_players = []

        while True:
            """loop until user does not want to add any more players. Displays the options to the user
            and gets their input"""
            option = ActiveTournamentView.register_players_options()

            # if user selects by entering player number from list
            if option.isdigit() and 1 <= int(option) <= len(list_of_players):
                selected_tournament_players.append(list_of_players[int(option) - 1])
                print(f"Added {list_of_players[int(option) - 1].get('name')} to the tournament.")

            # if user enters id of the user
            elif option.lower() == 'id':
                chess_id = input("Enter Chess ID: ").strip()
                player = search_by_id(chess_id)
                if player:
                    selected_tournament_players.append(player)
                    print(f"Added {player.get('name')} to the tournament.")
                else:
                    print("No players match that Chess ID.")

            # if user enters player name or portion of name. Able to select from the returned list
            elif option.lower() == 'name':
                name = input("Enter the name of the player: ")
                matching_names = search_by_name(name)
                if matching_names:
                    # case where multiple players match the name
                    print("Players found:")
                    for i, player in enumerate(matching_names, 1):
                        print(f"{i}. {player.get('name')}")
                    selection = input("Select the player number to add: ")
                    # selects number of player from list of returned names that matched
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
                # prints error message for any other user input
                print("ERROR: Select the correct Player number or the correct 'keyword' to add players.")

        # add the registered players to the empty list
        tournament.add_players(selected_tournament_players)

        # create initial pairings/matches randomly and print out the pairing results to the user
        matches = Matches.pair_randomly(tournament)

        print("\nGenerated Round 1 Pairs: ")
        print("------------------------")
        for pair in matches:
            player1_id = pair["players"][0]
            player2_id = pair["players"][1]
            print(f"-- {player1_id} vs. {player2_id} --")

        # save the tournament object with all the new information
        tournament.save()
        print("First round matches have been set. Returning to Tournament Options screen...")

    @staticmethod
    def enter_results(tournament):
        """This method gives the user access to entering the results of the matches of the tournament.
        method goes by rounds and displays the information from every round and allows the user to enter
        results from the outcomes of each round"""

        if tournament.is_completed:
            print("ERROR: The Tournament is completed. There are no more rounds.")
            return

        print("-" * 74)
        print(f"{' ' * 15}-- ENTERING ROUND {tournament.current_round}/{tournament.number_of_rounds} RESULTS --")

        # this will hold the matches in the current round that are not completed
        current_round_matches = []

        for match in tournament.rounds:
            if not match["completed"]:
                # adds all non completed matches from rounds to list
                current_round_matches.append(match)

        # displays the current matches in the round and who the opponents are
        print(f"\nCurrent matches in Round {tournament.current_round}:")
        for i, match in enumerate(current_round_matches, 1):
            player1, player2 = match['players']
            print(f"{i}. {player1} vs. {player2}")

        # for every match that is not completed, user will be able to enter the chess id of winner, or 'draw' for tie
        for match in current_round_matches:
            # print(f"Processing round: {match}")
            print(f"\n * MATCH: {match['players'][0]} vs {match['players'][1]} *")
            print("-" * 31)

            if not match["completed"]:
                while True:
                    winner = input("Enter the Chess ID of the player who won this match (or 'Draw' for a draw): ")
                    # if match ended as a draw, set winner as None, complete is True and give each player 0.5 points
                    if winner.lower() == 'draw':
                        match['winner'] = None  # Mark the match as a draw
                        match['completed'] = True
                        print("Match ended as a DRAW, both players will receive 0.5 points.")
                        tournament.update_points(match['players'], 0.5)
                        break
                    elif winner in match["players"]:
                        # if the entered chess_id matches any player in the round, we will give player 1 point and
                        # set them as winner
                        match['winner'] = winner
                        match['completed'] = True
                        print(f"{winner} won this match, player will receive 1 point.")
                        tournament.update_points([winner], 1)
                        break
                    else:
                        # if wrong chess_id is entered or draw is not entered, have user repeat entry
                        print("Invalid input. Please enter a valid player ID or 'Draw' if players tied.")

            # if round of matches were the last round, we will set as tournament is finished = True, complete = True
            if (tournament.current_round == tournament.number_of_rounds and
                    all(match["completed"] for match in tournament.rounds)):
                tournament.is_finished = True
                tournament.is_completed = True
                print("\nTournament is now completed. Tournament can now be found on 'View All Completed Tournaments'")

        # prints the player points after each round by descending order
        print("\nCurrent Leaderboard")
        print("--------------------")
        # Sort players based on points in descending order
        sorted_players = sorted(tournament.points.items(), key=lambda item: item[1], reverse=True)
        for player, points in sorted_players:
            print(f"{player}: {points}")

        # save the tournament with new information
        tournament.save()
        # automatically return to menu options for tournament
        print("Returning to 'Active Tournament Options' Menu...")

    @staticmethod
    def advance_to_next_round(tournament):
        """this method advances the tournament to the next round after results were entered and user advances rounds"""
        if tournament.is_completed:
            print("ERROR: The Tournament is completed. There are no more rounds.")
            return

        while True:
            confirmation = input("Are you sure you want to advance to the next round? (yes/no): ").lower()

            if confirmation == "no":
                print("Round advancement is canceled. Returning to Active Tournament Options Menu...")
                break

            # increase tournament round by 1 if user selects yes
            elif confirmation == "yes":
                tournament.current_round += 1

            # if current round is greater than total rounds, the tournament has been completed
                if tournament.current_round > tournament.number_of_rounds:
                    print("Tournament has already reached its last round.")
                    print("Returning to Active Tournament Options Menu...")
                    tournament.current_round = tournament.number_of_rounds
                    break

                # DEBUG: print("Before generating match pairs:", tournament.rounds)

                # create new pairing based on points
                matches = Matches.pair_based_on_points(tournament)

                # DEBUG: print("After generating match pairs:", tournament.rounds)

                # print the new matches that were generated from method
                print(f"\nGenerated Round {tournament.current_round} Pairs: ")
                print("-------------------------")
                for pair in matches:
                    player1_id = pair["players"][0]
                    player2_id = pair["players"][1]
                    print(f"-- {player1_id} vs. {player2_id} --")

                # Save the tournament state
                tournament.save()
                print(f"Tournament advanced to Round {tournament.current_round}. Returning to 'Active Tournament "
                      f"Options' Menu")
                break
            else:
                print("ERROR: Enter 'yes' or 'no")

    @staticmethod
    def generate_report(tournament):
        """this method generates the report when tournament is recently completed. User must complete the
        entire tournament before getting access to the report"""
        if not tournament.is_completed:
            print("ERROR: Tournament needs to be completed in order to generate a report.")
            return
        else:
            ActiveTournamentView.display_report(tournament)
