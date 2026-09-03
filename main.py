from datetime import datetime

# ==============================
#       ATM ACCOUNT DATA
# ==============================

user_pin = "1234"
account_balance = 50000.0
transaction_history = []

valid_recipient = "987654321"

# Extra Features
MAX_DAILY_WITHDRAW = 25000.0
withdrawn_today = 0.0

ADMIN_CODE = "9999"


# ==============================
#       LOGIN FUNCTION
# ==============================

def login_user():
    tries = 3

    print("\n================================")
    print("       WELCOME TO OUR ATM")
    print("================================")

    while tries > 0:
        entered = input("Enter your 4-digit PIN: ")

        if len(entered) != 4 or not entered.isdigit():
            print("Invalid PIN! Enter exactly 4 numbers.")
            continue

        if entered == user_pin:
            print("Login successful! Welcome.")
            return True

        tries -= 1

        if tries > 0:
            print(f"Wrong PIN! {tries} attempt(s) remaining.")
        else:
            print("Too many incorrect attempts.")
            print("Your account has been locked.")

    return False


# ==============================
#       BALANCE CHECK
# ==============================

def show_balance():
    print(f"\nYour available balance is: Rs. {account_balance:,.2f}")


# ==============================
#       RECEIPT
# ==============================

def print_receipt(transaction_name, money):
    answer = input("\nWould you like a receipt? (y/n): ").lower()

    if answer == "y":
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        print("\n========================================")
        print("          NATIONAL BANK ATM")
        print("========================================")
        print(f"Date & Time : {current_time}")
        print(f"Transaction: {transaction_name}")
        print(f"Amount     : Rs. {money:,.2f}")
        print(f"Balance    : Rs. {account_balance:,.2f}")
        print("========================================")
        print("       Thank you for banking with us")
        print("========================================")


# ==============================
#       DEPOSIT
# ==============================

def add_money():
    global account_balance

    try:
        money = float(input("\nEnter amount to deposit: Rs. "))

        if money <= 0:
            print("Deposit amount must be greater than zero.")
            return

        account_balance += money

        transaction_history.append({
            "type": "Deposit",
            "amount": money,
            "sign": "+",
            "time": datetime.now().strftime("%d-%m-%Y %H:%M")
        })

        print(f"Rs. {money:,.2f} deposited successfully.")
        print(f"New balance: Rs. {account_balance:,.2f}")

        print_receipt("Deposit", money)

    except ValueError:
        print("Invalid input! Please enter a numeric amount.")


# ==============================
#       WITHDRAW
# ==============================

def take_money():
    global account_balance, withdrawn_today

    try:
        money = float(input("\nEnter amount to withdraw: Rs. "))

        if money <= 0:
            print("Withdrawal amount must be greater than zero.")
            return

        if withdrawn_today + money > MAX_DAILY_WITHDRAW:
            left = MAX_DAILY_WITHDRAW - withdrawn_today
            print("Daily withdrawal limit exceeded.")
            print(f"You can withdraw only Rs. {left:,.2f} more today.")
            return

        if money > account_balance:
            print("Transaction failed!")
            print("You do not have enough balance.")
            return

        account_balance -= money
        withdrawn_today += money

        transaction_history.append({
            "type": "Withdrawal",
            "amount": money,
            "sign": "-",
            "time": datetime.now().strftime("%d-%m-%Y %H:%M")
        })

        print(f"Rs. {money:,.2f} withdrawn successfully.")
        print(f"Remaining balance: Rs. {account_balance:,.2f}")

        print_receipt("Withdrawal", money)

    except ValueError:
        print("Invalid input! Please enter a numeric amount.")


# ==============================
#       MONEY TRANSFER
# ==============================

def send_money():
    global account_balance

    receiver = input("\nEnter recipient account number: ")

    if receiver != valid_recipient:
        print("Invalid account number!")
        print("Recipient account was not found.")
        return

    try:
        money = float(input("Enter amount to transfer: Rs. "))

        if money <= 0:
            print("Transfer amount must be greater than zero.")
            return

        if money > account_balance:
            print("Transfer failed!")
            print("Insufficient balance.")
            return

        account_balance -= money

        transaction_history.append({
            "type": "Transfer",
            "amount": money,
            "sign": "-",
            "time": datetime.now().strftime("%d-%m-%Y %H:%M")
        })

        print(f"Rs. {money:,.2f} transferred successfully.")
        print(f"Recipient Account: {receiver}")
        print(f"Remaining balance: Rs. {account_balance:,.2f}")

        print_receipt("Money Transfer", money)

    except ValueError:
        print("Invalid input! Please enter a numeric amount.")


# ==============================
#       CHANGE PIN
# ==============================

def update_pin():
    global user_pin

    old_pin = input("\nEnter your current PIN: ")

    if old_pin != user_pin:
        print("Incorrect current PIN.")
        return

    new_pin = input("Enter your new 4-digit PIN: ")

    if len(new_pin) != 4 or not new_pin.isdigit():
        print("New PIN must contain exactly 4 digits.")
        return

    confirm = input("Confirm your new PIN: ")

    if new_pin != confirm:
        print("PIN confirmation does not match.")
        return

    user_pin = new_pin
    print("Your PIN has been changed successfully.")


# ==============================
#       MINI STATEMENT
# ==============================

def show_statement():

    print("\n========== MINI STATEMENT ==========")

    if not transaction_history:
        print("No transactions available.")

    else:
        print(f"{'Date & Time':<18} {'Transaction':<15} {'Amount':>12}")
        print("-----------------------------------------------")

        for item in transaction_history[-5:]:
            amount = f"{item['sign']}{item['amount']:,.2f}"

            print(
                f"{item['time']:<18} "
                f"{item['type']:<15} "
                f"{amount:>12}"
            )

    print("-----------------------------------------------")
    print(f"Current Balance: Rs. {account_balance:,.2f}")
    print("===============================================")


# ==============================
#       ADMIN PANEL
# ==============================

def admin_panel():

    print("\n========== ADMIN PANEL ==========")
    print(f"Account Balance : Rs. {account_balance:,.2f}")
    print(f"Total Transactions: {len(transaction_history)}")
    print(f"User PIN        : {user_pin}")

    print("---------------------------------")

    if not transaction_history:
        print("No transactions have been made.")
    else:
        print("Recent Transactions:")

        for number, item in enumerate(transaction_history, start=1):
            print(
                f"{number}. "
                f"{item['time']} | "
                f"{item['type']} | "
                f"Rs. {item['amount']:,.2f}"
            )

    print("=================================")
    input("Press Enter to return...")


# ==============================
#       ATM MENU
# ==============================

def start_atm():

    while True:

        print("\n========== ATM MACHINE ==========")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Change PIN")
        print("6. Mini Statement")
        print("7. Logout")
        print("8. Exit")
        print("=================================")

        option = input("Select an option: ")

        if option == "1":
            show_balance()

        elif option == "2":
            add_money()

        elif option == "3":
            take_money()

        elif option == "4":
            send_money()

        elif option == "5":
            update_pin()

        elif option == "6":
            show_statement()

        elif option == "7":
            print("\nYou have been logged out successfully.")
            return "logout"

        elif option == "8":
            print("\nThank you for using our ATM.")
            print("Please take your card.")
            return "exit"

        else:
            print("Invalid option! Please select 1 to 8.")


# ==============================
#       MAIN PROGRAM
# ==============================

if __name__ == "__main__":

    while True:

        entered_pin = input("\nEnter PIN to continue: ")

        # Admin Login
        if entered_pin == ADMIN_CODE:
            admin_panel()
            continue

        # Normal User Login
        if entered_pin == user_pin:

            print("\nLogin successful!")

            result = start_atm()

            if result == "exit":
                break

        else:
            print("Incorrect PIN!")

            # Give the user 3 attempts
            success = False

            for attempt in range(2):
                entered_pin = input("Enter PIN again: ")

                if entered_pin == user_pin:
                    success = True
                    break

                print("Incorrect PIN!")

            if success:
                result = start_atm()

                if result == "exit":
                    break
            else:
                print("\nMaximum attempts reached.")
                print("Account locked for this session.")
                break