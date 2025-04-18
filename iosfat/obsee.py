import random


MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}
symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
}

def did_you_win(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines

def get_slot_machine(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)
    return columns

def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end = " | ")
            else:
                print(column[row], end="" )
        print()


def deposit():
    while True:
        amount = input("What would you like to deposit? ")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Brokie, must be greater than 0")
        else:
            print("")
    return amount

def get_num_lines():
    while True:
        lines = input("How many lines do you want?")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("What are you even doing here")
        else:
            print("")

    return lines


def get_bet():
    while True:
        amount = input("What would you like to bet on each line? ")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Brokie, must be greater than 0 {MIN_BET} and {MAX_BET}")
        else:
            print("")
    return amount



    


def main():
    balance = deposit()
    lines = get_num_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print("Too broke mane")
        else:
            break
    
    print(f"You are betting ${bet} on {lines}. Total bet is equal to: ${total_bet}")

    slots = get_slot_machine(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = did_you_win(slots, lines, bet, symbol_value)
    print(f"You won {winnings}. ")
    if winnings != 0:
        print(f"You won on line(s): ", *winning_lines)
    else:
        print("LOL!!")

   
    

    
play = input("Do you want to gamble (Y/N)")
if play == "Y":
    while True:
        main()
else:
    print(f"ok.")
