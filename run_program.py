import json
import os
from models.tournament import Tournament
from manage_clubs import App

while True:
    print("--------------------------------------------------------------------------")
    print("|             ** WELCOME TO THE CHESS TOURNAMENT MANAGER **              |")
    print("--------------------------------------------------------------------------")
    print("                         - MAIN MENU -\n")
    print("1: View all Clubs and Club Members / Create New Club and Club Members")
    print("2: Create New Tournament and Register Players")
    print("3: View/Manage all active tournaments")
    print("4: View all completed tournaments")
    print("\n5: Exit application")

    print("--------------------------------------------------------------------------")
    user_choice = input("Enter your choice between 1 - 4 or 5 to exit application: ")

    if user_choice.isdigit() and user_choice == "1":
        app = App()
        app.run()
    elif user_choice.isdigit() and user_choice == "2":
        Tournament.create_tournament()
    elif user_choice.isdigit() and user_choice == "5":
        print("You are now exiting the Chess Tournament Manager program...")
        break
    else:
        print("Invalid choice. Please choose 1 - 4 or 'E' to exit")
