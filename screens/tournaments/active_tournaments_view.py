from operator import itemgetter
from datetime import datetime


class ActiveTournamentView:
    def __init__(self, tournament):
        self.tournament = tournament

    @staticmethod
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
            print()
            print("-" * 74)
            print(f"{' '*20}-- ACTIVE TOURNAMENT(s) --\n")

            for i, (file_name, start_date) in enumerate(active_tournaments_dates, start=1):
                print(f"{i}. {file_name} - Start Date: {start_date.strftime('%d-%m-%Y')}")

            return active_tournaments_dates
        else:
            print("There are no active tournaments.")

    @staticmethod
    def display_all_players(players):
        print()
        print("-" * 74)
        print(f"{' '*20}-- ALL PLAYERS --\n")
        for i, player in enumerate(players, start=1):
            print(f"{i}. {player}")

    @staticmethod
    def display_tournament_information(tournament):
        print(f"\n{' '*20}-- CURRENT TOURNAMENT INFORMATION --\n")
        print(f"Name: {tournament.name}")
        print(f"Start Date: {tournament.start_date}")
        print(f"End Date: {tournament.end_date}")
        print(f"Venue: {tournament.venue}")
        print(f"Number of Rounds: {tournament.number_of_rounds}")
        print(f"Current Round: {tournament.current_round}")
        print(f"Completed: {tournament.is_completed}")
        # Display Players
        print("Players:")
        for player in tournament.registered_players:
            print(f" - {player['name']} - ({player['chess_id']})")
        print(f"Finished: {tournament.is_finished}")
        # Display Rounds
        print("Rounds:")
        for i, match in enumerate(tournament.rounds, 1):
            print(f" - Match: {match['players'][0]} vs. {match['players'][1]}")
            print(f" - Winner: {match['winner']}")

    @staticmethod
    def get_tournament_choice():
        print("\nSelect a tournament number to view/modify or Enter 'X' to go back to the main menu")
        choice = input("Enter your choice: ")
        return choice

    @staticmethod
    def active_tournament_options_choice():
        print()
        print("-" * 74)
        print(f"{' '*20}-- ACTIVE TOURNAMENT OPTIONS --\n")
        print("1. Register a player for the currently selected tournament")
        print("2. Enter results of the match for the current round")
        print("3. Advance to the next round")
        print("4. Generate a tournament report")
        print("5. Return to the Active Tournaments List Menu")

        user_choice = input("\nEnter your choice: ")

        return user_choice

    @staticmethod
    def register_players_options():
        print()
        print("-" * 74)
        print("Type the number associated with the player you would like to add to the tournament or ")
        print("Type 'ID' to search for a player by Chess ID or ")
        print("Type 'Name' to search for a player by Name or ")
        print("Type 'X' to finish registering players and/or to return to Tournament options")

        choice = input("\nYour choice is: ")
        return choice

    @staticmethod
    def display_report(tournament):
        print()
        print("-" * 74)
        print(f"{' ' * 20}-- '{tournament.name}' TOURNAMENT REPORT --")

        # Display basic tournament information
        print(f"\nTournament Name: {tournament.name}")
        print(f"Venue: {tournament.venue}")

        print(f"\nStart Date: {tournament.start_date}")
        print(f"End Date: {tournament.end_date}")

        print(f"\nTotal Number of Rounds: {tournament.number_of_rounds}")
        print(f"Total Number of Players: {len(tournament.registered_players)}")

        # Display players sorted by points descending
        print("\nPlayer Score Rankings:")
        print("----------------------------")
        sorted_players = sorted(tournament.points.items(), key=lambda item: item[1], reverse=True)
        for player, points in sorted_players:
            print(f"{player}: {points}")

        # Display rounds and matches
        print("\nMatches:")
        print("--------------------")
        # print("DEBUG - Rounds data structure:")
        # print(tournament.rounds)
        for i, match in enumerate(tournament.rounds, 1):
            print(f"\n-- Match {i} --")
            print(f"Match: {match['players'][0]} vs. {match['players'][1]}")
            print(f"Winner: {match['winner']}")

        print("\n** End of Tournament Report **")
