from operator import itemgetter
from datetime import datetime


class CompletedTournamentView:
    def __init__(self, tournament):
        self.tournament = tournament

    @staticmethod
    def display_completed_tournaments(completed_tournaments):
        """This function displays the active tournaments found from earliest to oldest based on start date"""
        if len(completed_tournaments) >= 1:
            # list to hold all tournament name and start_date as date object to sort
            completed_tournaments_dates = []

            # iterate through active_tournaments to convert string date to object date
            for file_name, end_date in completed_tournaments:
                date_obj = datetime.strptime(end_date, "%d-%m-%Y").date()
                completed_tournaments_dates.append((file_name, date_obj))

            # sort dates from earliest to oldest
            completed_tournaments_dates.sort(key=itemgetter(1), reverse=True)

            # print sorted active tournaments with string dates
            print()
            print("-" * 74)
            print(f"{' '*20}-- COMPLETED TOURNAMENT(s) --\n")

            for i, (file_name, start_date) in enumerate(completed_tournaments_dates, start=1):
                print(f"{i}. {file_name} - End Date: {start_date.strftime('%d-%m-%Y')}")

            return completed_tournaments_dates
        else:
            print("There are no completed tournaments.")

    @staticmethod
    def display_tournament_information(tournament):
        print(f"\n{' ' * 20}-- CURRENT TOURNAMENT INFORMATION --\n")
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
    def completed_tournament_options_choice():
        print()
        print("-" * 74)
        print(f"{' ' * 20}-- COMPLETED TOURNAMENT OPTIONS --\n")
        print("1. Generate a tournament report")
        print("2. Return to the Completed Tournaments List Menu")

        user_choice = input("\nEnter your choice: ")

        return user_choice

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
