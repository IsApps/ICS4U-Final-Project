import tkinter as tk
from tkinter import messagebox
import random
import json
import os

SAVE_FILE = "stonks_save.json"


class Stock:
    def __init__(self, symbol, name, price):
        self.symbol = symbol
        self.name = name
        self.price = price
        self.history = [price]

    def update_price(self):
        trend = self.get_trend()
        random_change = random.uniform(-2.5, 2.5)
        percent_change = random_change + trend

        self.price += self.price * (percent_change / 100)

        if self.price < 1:
            self.price = 1

        self.history.append(self.price)

        if len(self.history) > 45:
            self.history.pop(0)

    def get_trend(self):
        if len(self.history) < 3:
            return 0

        if self.history[-1] > self.history[-2]:
            return 0.45
        elif self.history[-1] < self.history[-2]:
            return -0.45
        return 0

    def moving_average(self):
        recent = self.history[-5:]
        return sum(recent) / len(recent)


class Portfolio:
    def __init__(self, cash=10000):
        self.cash = cash
        self.holdings = {}

    def buy(self, stock, quantity):
        cost = stock.price * quantity

        if quantity <= 0:
            return False, "Quantity must be greater than 0."

        if cost > self.cash:
            return False, "Not enough cash."

        self.cash -= cost
        self.holdings[stock.symbol] = self.holdings.get(stock.symbol, 0) + quantity
        return True, f"Bought {quantity} shares of {stock.symbol}"

    def sell(self, stock, quantity):
        owned = self.holdings.get(stock.symbol, 0)

        if quantity <= 0:
            return False, "Quantity must be greater than 0."

        if quantity > owned:
            return False, "Not enough shares owned."

        self.cash += stock.price * quantity
        self.holdings[stock.symbol] -= quantity

        if self.holdings[stock.symbol] == 0:
            del self.holdings[stock.symbol]

        return True, f"Sold {quantity} shares of {stock.symbol}"

    def total_value(self, stocks):
        total = self.cash

        for symbol, quantity in self.holdings.items():
            if symbol in stocks:
                total += stocks[symbol].price * quantity

        return total


class AITrader:
    def __init__(self):
        self.portfolio = Portfolio(10000)

    def trade(self, stocks):
        for stock in stocks.values():
            average = stock.moving_average()

            if stock.price < average * 0.985:
                self.portfolio.buy(stock, 1)
            elif stock.price > average * 1.025:
                self.portfolio.sell(stock, 1)


class StonksApp:
    def __init__(self, root):
        self.root = root
        self.root.title("STONKS")
        self.root.geometry("1250x760")
        self.root.configure(bg="#0b0f19")

        self.bg = "#0b0f19"
        self.card = "#111827"
        self.card_light = "#172033"
        self.text = "#f8fafc"
        self.muted = "#94a3b8"
        self.border = "#1f2937"
        self.green = "#22c55e"
        self.red = "#ef4444"
        self.blue = "#3b82f6"

        self.selected_symbol = "AAPL"

        self.stocks = {
            "AAPL": Stock("AAPL", "Apple Inc.", 180),
            "TSLA": Stock("TSLA", "Tesla Inc.", 250),
            "NVDA": Stock("NVDA", "Nvidia Corp.", 900),
            "AMZN": Stock("AMZN", "Amazon Inc.", 190),
            "MSFT": Stock("MSFT", "Microsoft Corp.", 420)
        }

        self.user = Portfolio(10000)
        self.bot = AITrader()

        self.build_ui()
        self.refresh_ui()

    def create_card(self, parent):
        return tk.Frame(
            parent,
            bg=self.card,
            highlightbackground=self.border,
            highlightthickness=1
        )

    def build_ui(self):
        header = tk.Frame(self.root, bg=self.bg)
        header.pack(fill="x", padx=28, pady=(24, 14))

        title_frame = tk.Frame(header, bg=self.bg)
        title_frame.pack(side="left")

        tk.Label(
            title_frame,
            text="STONKS",
            font=("Segoe UI", 28, "bold"),
            bg=self.bg,
            fg=self.text
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="Professional Stock Market Simulator",
            font=("Segoe UI", 11),
            bg=self.bg,
            fg=self.muted
        ).pack(anchor="w")

        self.account_label = tk.Label(
            header,
            text="",
            font=("Segoe UI", 13, "bold"),
            bg=self.bg,
            fg=self.green
        )
        self.account_label.pack(side="right", pady=18)

        main = tk.Frame(self.root, bg=self.bg)
        main.pack(fill="both", expand=True, padx=28, pady=(0, 28))

        self.market_panel = self.create_card(main)
        self.market_panel.pack(side="left", fill="y", padx=(0, 18))

        self.chart_panel = self.create_card(main)
        self.chart_panel.pack(side="left", fill="both", expand=True)

        self.portfolio_panel = self.create_card(main)
        self.portfolio_panel.pack(side="right", fill="y", padx=(18, 0))

        self.build_market_panel()
        self.build_chart_panel()
        self.build_portfolio_panel()

    def build_market_panel(self):
        tk.Label(
            self.market_panel,
            text="Market",
            font=("Segoe UI", 16, "bold"),
            bg=self.card,
            fg=self.text
        ).pack(anchor="w", padx=20, pady=(20, 5))

        tk.Label(
            self.market_panel,
            text="Live market prices",
            font=("Segoe UI", 10),
            bg=self.card,
            fg=self.muted
        ).pack(anchor="w", padx=20, pady=(0, 14))

        self.stock_buttons = {}

        for symbol in self.stocks:
            button = tk.Button(
                self.market_panel,
                text="",
                font=("Segoe UI", 11, "bold"),
                bg=self.card_light,
                fg=self.text,
                activebackground="#22304a",
                activeforeground=self.text,
                relief="flat",
                bd=0,
                width=28,
                height=3,
                anchor="w",
                justify="left",
                padx=14,
                command=lambda s=symbol: self.select_stock(s)
            )
            button.pack(fill="x", padx=16, pady=6)
            self.stock_buttons[symbol] = button

    def build_chart_panel(self):
        top = tk.Frame(self.chart_panel, bg=self.card)
        top.pack(fill="x", padx=22, pady=(20, 8))

        self.stock_title = tk.Label(
            top,
            text="",
            font=("Segoe UI", 21, "bold"),
            bg=self.card,
            fg=self.text
        )
        self.stock_title.pack(side="left")

        self.price_label = tk.Label(
            top,
            text="",
            font=("Segoe UI", 15, "bold"),
            bg=self.card
        )
        self.price_label.pack(side="right")

        self.stock_subtitle = tk.Label(
            self.chart_panel,
            text="",
            font=("Segoe UI", 10),
            bg=self.card,
            fg=self.muted
        )
        self.stock_subtitle.pack(anchor="w", padx=22)

        self.canvas = tk.Canvas(
            self.chart_panel,
            bg=self.card,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=16, pady=16)

    def build_portfolio_panel(self):
        tk.Label(
            self.portfolio_panel,
            text="Portfolio",
            font=("Segoe UI", 16, "bold"),
            bg=self.card,
            fg=self.text
        ).pack(anchor="w", padx=20, pady=(20, 5))

        tk.Label(
            self.portfolio_panel,
            text="Your current investments",
            font=("Segoe UI", 10),
            bg=self.card,
            fg=self.muted
        ).pack(anchor="w", padx=20, pady=(0, 14))

        self.cash_label = tk.Label(
            self.portfolio_panel,
            text="",
            font=("Segoe UI", 11),
            bg=self.card,
            fg=self.muted
        )
        self.cash_label.pack(anchor="w", padx=20)

        self.total_label = tk.Label(
            self.portfolio_panel,
            text="",
            font=("Segoe UI", 17, "bold"),
            bg=self.card,
            fg=self.text
        )
        self.total_label.pack(anchor="w", padx=20, pady=(4, 18))

        tk.Label(
            self.portfolio_panel,
            text="Quantity",
            font=("Segoe UI", 10, "bold"),
            bg=self.card,
            fg=self.muted
        ).pack(anchor="w", padx=20)

        self.quantity_entry = tk.Entry(
            self.portfolio_panel,
            font=("Segoe UI", 13),
            justify="center",
            bg="#0b1220",
            fg=self.text,
            insertbackground=self.text,
            relief="flat"
        )
        self.quantity_entry.pack(fill="x", padx=20, pady=(7, 14), ipady=10)
        self.quantity_entry.insert(0, "1")

        tk.Button(
            self.portfolio_panel,
            text="BUY",
            font=("Segoe UI", 12, "bold"),
            bg=self.green,
            fg="#052e16",
            activebackground="#16a34a",
            relief="flat",
            bd=0,
            command=self.buy_stock
        ).pack(fill="x", padx=20, pady=5, ipady=10)

        tk.Button(
            self.portfolio_panel,
            text="SELL",
            font=("Segoe UI", 12, "bold"),
            bg=self.red,
            fg="#450a0a",
            activebackground="#dc2626",
            relief="flat",
            bd=0,
            command=self.sell_stock
        ).pack(fill="x", padx=20, pady=5, ipady=10)

        tk.Button(
            self.portfolio_panel,
            text="NEXT MARKET TICK",
            font=("Segoe UI", 11, "bold"),
            bg=self.blue,
            fg="white",
            activebackground="#2563eb",
            relief="flat",
            bd=0,
            command=self.market_tick
        ).pack(fill="x", padx=20, pady=(18, 8), ipady=10)

        buttons = tk.Frame(self.portfolio_panel, bg=self.card)
        buttons.pack(fill="x", padx=20)

        tk.Button(
            buttons,
            text="SAVE",
            font=("Segoe UI", 10, "bold"),
            bg=self.card_light,
            fg=self.text,
            relief="flat",
            bd=0,
            command=self.save_game
        ).pack(side="left", expand=True, fill="x", padx=(0, 4), ipady=8)

        tk.Button(
            buttons,
            text="LOAD",
            font=("Segoe UI", 10, "bold"),
            bg=self.card_light,
            fg=self.text,
            relief="flat",
            bd=0,
            command=self.load_game
        ).pack(side="right", expand=True, fill="x", padx=(4, 0), ipady=8)

        tk.Label(
            self.portfolio_panel,
            text="Holdings",
            font=("Segoe UI", 12, "bold"),
            bg=self.card,
            fg=self.text
        ).pack(anchor="w", padx=20, pady=(18, 8))

        self.holdings_label = tk.Label(
            self.portfolio_panel,
            text="",
            font=("Segoe UI", 10),
            bg=self.card,
            fg=self.muted,
            justify="left"
        )
        self.holdings_label.pack(anchor="w", padx=20)

    def get_stock_change(self, stock):
        if len(stock.history) < 2:
            return 0, 0

        change = stock.history[-1] - stock.history[-2]
        percent = (change / stock.history[-2]) * 100

        return change, percent

    def select_stock(self, symbol):
        self.selected_symbol = symbol
        self.market_tick()

    def market_tick(self):
        for stock in self.stocks.values():
            stock.update_price()

        self.bot.trade(self.stocks)
        self.refresh_ui()

    def buy_stock(self):
        try:
            quantity = int(self.quantity_entry.get())
            stock = self.stocks[self.selected_symbol]

            success, message = self.user.buy(stock, quantity)

            if success:
                messagebox.showinfo("Trade Successful", message)
            else:
                messagebox.showerror("Trade Failed", message)

            self.market_tick()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def sell_stock(self):
        try:
            quantity = int(self.quantity_entry.get())
            stock = self.stocks[self.selected_symbol]

            success, message = self.user.sell(stock, quantity)

            if success:
                messagebox.showinfo("Trade Successful", message)
            else:
                messagebox.showerror("Trade Failed", message)

            self.market_tick()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def refresh_ui(self):
        total = self.user.total_value(self.stocks)

        self.account_label.config(text=f"Portfolio Value  ${total:,.2f}")
        self.cash_label.config(text=f"Cash Balance: ${self.user.cash:,.2f}")
        self.total_label.config(text=f"${total:,.2f}")

        for symbol, button in self.stock_buttons.items():
            stock = self.stocks[symbol]
            change, percent = self.get_stock_change(stock)

            marker = "+" if percent >= 0 else ""

            button.config(
                text=(
                    f"{symbol}    ${stock.price:,.2f}\n"
                    f"{marker}{percent:.2f}%    {stock.name}"
                )
            )

            if symbol == self.selected_symbol:
                button.config(bg="#1d4ed8")
            else:
                button.config(bg=self.card_light)

        stock = self.stocks[self.selected_symbol]
        change, percent = self.get_stock_change(stock)

        colour = self.green if percent >= 0 else self.red
        marker = "+" if percent >= 0 else ""

        self.stock_title.config(text=stock.symbol)

        self.stock_subtitle.config(
            text=f"{stock.name} • Moving Average ${stock.moving_average():,.2f}"
        )

        self.price_label.config(
            text=f"${stock.price:,.2f}   {marker}{percent:.2f}%",
            fg=colour
        )

        if not self.user.holdings:
            holdings_text = "No stocks owned."
        else:
            holdings_text = ""

            for symbol, quantity in self.user.holdings.items():
                stock = self.stocks[symbol]
                value = stock.price * quantity

                holdings_text += (
                    f"{symbol} | Shares: {quantity}\n"
                    f"Price: ${stock.price:,.2f}\n"
                    f"Value: ${value:,.2f}\n\n"
                )

        self.holdings_label.config(text=holdings_text)
        self.draw_chart(stock)

    def draw_chart(self, stock):
        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 100 or height < 100:
            self.root.after(100, lambda: self.draw_chart(stock))
            return

        padding = 60
        prices = stock.history

        max_price = max(prices)
        min_price = min(prices)

        if max_price == min_price:
            max_price += 1
            min_price -= 1

        chart_width = width - padding * 2
        chart_height = height - padding * 2

        for i in range(6):
            y = padding + i * chart_height / 5

            self.canvas.create_line(
                padding,
                y,
                width - padding,
                y,
                fill="#1f2937"
            )

        points = []

        for i, price in enumerate(prices):
            x = padding + i * chart_width / max(1, len(prices) - 1)
            y = padding + ((max_price - price) / (max_price - min_price)) * chart_height
            points.append((x, y))

        line_colour = self.green if prices[-1] >= prices[0] else self.red

        for i in range(len(points) - 1):
            self.canvas.create_line(
                points[i][0],
                points[i][1],
                points[i + 1][0],
                points[i + 1][1],
                fill=line_colour,
                width=3,
                smooth=True
            )

        if points:
            x, y = points[-1]

            self.canvas.create_oval(
                x - 5,
                y - 5,
                x + 5,
                y + 5,
                fill=line_colour,
                outline=line_colour
            )

            self.canvas.create_text(
                x - 10,
                y - 18,
                text=f"${prices[-1]:,.2f}",
                fill=line_colour,
                font=("Segoe UI", 10, "bold")
            )

    def save_game(self):
        data = {
            "cash": self.user.cash,
            "holdings": self.user.holdings,
            "stocks": {}
        }

        for symbol, stock in self.stocks.items():
            data["stocks"][symbol] = {
                "price": stock.price,
                "history": stock.history
            }

        try:
            with open(SAVE_FILE, "w") as file:
                json.dump(data, file, indent=4)

            messagebox.showinfo("Saved", "Game saved successfully.")

        except IOError:
            messagebox.showerror("Error", "Could not save game.")

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            messagebox.showerror("Error", "No save file found.")
            return

        try:
            with open(SAVE_FILE, "r") as file:
                data = json.load(file)

            self.user.cash = data["cash"]
            self.user.holdings = data["holdings"]

            for symbol, stock_data in data["stocks"].items():
                if symbol in self.stocks:
                    self.stocks[symbol].price = stock_data["price"]
                    self.stocks[symbol].history = stock_data["history"]

            messagebox.showinfo("Loaded", "Save file loaded successfully.")
            self.refresh_ui()

        except Exception:
            messagebox.showerror("Error", "Save file could not be loaded.")


root = tk.Tk()
app = StonksApp(root)
root.mainloop()
