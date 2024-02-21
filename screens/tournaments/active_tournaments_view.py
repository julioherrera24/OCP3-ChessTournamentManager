from operator import itemgetter
from datetime import datetime
class ActiveTournamentView():
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
            print("\n--------------------------------------------------------------------------")
            print("                  -- ACTIVE TOURNAMENT(s) --\n")

            for i, (file_name, start_date) in enumerate(active_tournaments_dates, start=1):
                print(f"{i}. {file_name} - Start Date: {start_date.strftime('%d-%m-%Y')}")

            return active_tournaments_dates
        else:
            print("There are no active tournaments.")
