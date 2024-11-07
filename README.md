# Dö.rand (do > random)

Dö.rand is a PyQt5-based random number rolling game where players compete to achieve the highest or lowest possible rolls, with each roll generating a random number that is 11 decimal places long. The goal is to roll either the highest or lowest number, and players create a username to submit their scores, which are then displayed on a local leaderboard.

## Requirements

- Python 3.x
- PyQt5 library
- Requests library

Install dependencies with:
```bash
pip install PyQt5 requests
```
or if you wanna make life hard, install `requirements.txt`

## Run
- Clone the repo
- Run the file "do.rand_server.py" and wait for initialization.
- Run the file "do.rand.py".
- To access the leaderboard, go to `localhost:5000`.
- Continue in the game window (do.rand.py)

## Play
- Enter a unique username not taken by anyone else
- Click "Roll Number"
- See if you roll a substantial high or low number. If you do, cool! If you don't, roll again.
- Check your local network's leaderboard at `localhost:5000`, which has entired based off usernames people entered. 

## Features

- **User Registration**: Choose a unique username to play.
- **Random Number Rolling**: Generate random numbers with a range of 0.00000000001 to 9.99999999999.
- **High and Low Score Tracking**: Track the highest and lowest rolls achieved.
- **Score Logging**: Log scores with timestamps in a local text file.
- **Cooldown Mechanism**: Prevents repeated rolling too quickly.
- **Confirmation Dialogs**: Ensures the user’s decisions with confirmation windows.
- **Leaderboard**: Accessible at `localhost:5000`, displays top scores **across the network**.
