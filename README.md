# OCP3-ChessTournamentManager

Chess Tournament Manager is a Python program that helps you organize and manage chess tournaments. The program allows you to create clubs and players, view, and manage active and completed tournaments.

## Prerequisites
- PyCharm
- Python 3.12.1
- [Flake8](https://flake8.pycqa.org/) for code linting

## Setting up PyCharm IDE
1. Go to [JetBrains PyCharm](https://www.jetbrains.com/pycharm/) version 3.12 and download the program for your given operating system.
2. Download Python from [python.org](https://www.python.org/downloads/) version 3.12.1 for your specific operating system.
3. Open PyCharm and create a new project.
4. Download the code.
5. Extract the code to your preferred location on your computer.
6. In the IDE, go to File > Open and navigate to the location where you extracted the code. Select `main.py`.

## Instructions for setting up and running program on Windows
1. Open Terminal
2. Download the files from this repository or create a clone using the code below.

   $ git clone https://github.com/julioherrera24/OCP3-ChessTournamentManager.git
   
3. Navigate to the directory containing this repository.

   $ cd OCP3-ChessTournamentManager
   
4. Create and activate a virtaul environment

   python -m venv env

   env/scripts/activate (to activate)
   
5. Install the necessary packages according to 'requirements.txt'

   pip install -r requirements.txt
   
6. Open and run the file 'main.py'

    .\main.py

## Instructions for setting up and running program on Mac
1. Open the command prompt/Terminal.
2. Download the files from this repository or create a clone using the code below.

   git clone https://github.com/julioherrera24/OCP3-ChessTournamentManager.git
   
3. Navigate to the directory containing this repository.

   cd OCP3-ChessTournamentManager

4. Create and activate a virtual environment.

   python -m venv env

   source env/bin/activate
   
5. Install the necessary packages according to 'requirements.txt'.

   python3 -m pip install -r requirements.txt

6. Open and run the file 'main.py'

   python3 main.py

## Generating a flake8 report
1. Navigate to the directory containing this repository based on your computer
   $ cd OCP3-ChessTournamentManager    (windows)
   cd OCP3-ChessTournament_Manager     (mac)
   
2. Run the following command
   $ flake8 --max-line-length 119 --format=html --htmldir=flake8_report    (windows)
   flake8 --max-line-length 119 --format=html --htmldir=flake8_report      (mac)

3. View report in the new flake8_report directory created in the repository





