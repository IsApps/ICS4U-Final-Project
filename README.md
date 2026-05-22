# ICS4U---Final-Project
This is our code for our project titled "Stonks". 

By: Ishan, Harkirat, and Punraj

---

About the Project

STONKS is a stock market simulator made in Python that lets users buy and sell stocks using virtual money. The goal of the project is to help people better understand how the stock market works without risking real money.

The program simulates stock price movement using random market changes and trend-based algorithms. Users can build their own portfolio, track profits/losses, and compete against an AI trading bot that automatically makes trading decisions.

This project was created for our Grade 12 Computer Science summative and focuses on concepts such as:
- Object-Oriented Programming
- Algorithms
- File I/O
- GUI Design
- Modular Programming
- Exception Handling

---

Features

• Simulated Stock Market
- Live stock price changes
- Stocks move using trend + randomization algorithms
- Different companies with unique prices

• Portfolio System
- Buy and sell stocks
- Track owned shares
- View portfolio value and cash balance

• AI Trading Bot
- AI automatically buys and sells stocks
- Uses moving averages and momentum detection
- Simulates real algorithmic trading

• Stock Graphs
- Live chart showing stock price history
- Green/red trend indicators
- Moving average calculations

• Save & Load System
- Saves user progress using JSON
- Stores:
  - Cash balance
  - Holdings
  - Stock prices
  - Market history

• GUI Interface
- Built using Tkinter
- Interactive buttons and menus
- Modern dark-themed design

---

Technologies Used

- Python 3
- Tkinter
- JSON
- Object-Oriented Programming
- File I/O

---

Classes Used

• Stock
Handles:
- Stock prices
- Price history
- Market trends
- Moving averages

• Portfolio
Handles:
- User cash
- Buying/selling stocks
- Holdings
- Total portfolio value

• AITrader
- Controls the AI trading bot and its decision-making system

• StonksApp
Handles:
- GUI
- Market updates
- Charts
- User interaction
- Save/load system

---

How the Program Works

- User selects a stock
- User enters quantity
- User buys or sells shares
- Market updates after every trade
- AI bot also trades automatically
- Stock prices continue changing over time

The market works using a custom algorithm that combines:
- Random price fluctuations
- Trend continuation
- Moving average analysis

This helps create more realistic stock behavior.

---

Error Handling

The program includes validation and exception handling to prevent crashes and invalid trades.

Examples:
- Cannot buy with insufficient funds
- Cannot sell stocks not owned
- Invalid quantities are rejected
- Save/load file errors are handled

---

Save File

The game stores data inside:

- stonks_save.json

This file keeps track of:
- User portfolio
- Cash balance
- Stock prices
- Stock history

---

Future Improvements

Some features we would add in the future:
- Multiplayer trading
- More stocks
- Cryptocurrency market
- Difficulty settings
- News/events affecting stocks
- Better AI strategies
- Login/account system

---

How to Run

1. Install Python 3
2. Download the project files
3. Run the program using:

python main.py

---

