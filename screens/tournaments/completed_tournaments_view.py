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
            print("\n--------------------------------------------------------------------------")
            print("                  -- COMPLETED TOURNAMENT(s) --\n")

            for i, (file_name, start_date) in enumerate(completed_tournaments_dates, start=1):
                print(f"{i}. {file_name} - End Date: {start_date.strftime('%d-%m-%Y')}")

            return completed_tournaments_dates
        else:
            print("There are no completed tournaments.")
