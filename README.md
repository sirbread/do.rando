# Dö.rand (do > random)

Dö.rand is a PyQt5-based random number rolling game where users compete to achieve the highest and lowest rolls possible. These rolls are computer generated numbers 11 decimal points long, and the end goal is to roll the highest or lowest number possible. Users create a username and submit their scores, which are displayed on a local leaderboard.

## Features

- **User Registration**: Choose a unique username to play.
- **Random Number Rolling**: Generate random numbers with a range of 0.00000000001 to 9.99999999999.
- **High and Low Score Tracking**: Track the highest and lowest rolls achieved.
- **Score Logging**: Log scores with timestamps in a local text file.
- **Cooldown Mechanism**: Prevents repeated rolling too quickly.
- **Confirmation Dialogs**: Ensures the user’s decisions with confirmation windows.
- **Leaderboard**: Accessible at `localhost:5000`, displays top scores **across the network**.

## Requirements

- Python 3.x
- PyQt5 library
- Requests library

Install dependencies with:
```bash
pip install PyQt5 requests
```

## Run
