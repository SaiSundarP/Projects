import sqlite3
import datetime

class DatabaseManager:
    def __init__(self, db_name='customer_record.db'):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

class BalanceManager(DatabaseManager):
    def check_balance(self, acno):
        self.cur.execute("SELECT balance FROM customer WHERE accno = ?;", (acno,))
        res = self.cur.fetchone()
        if res:
            return res[0]
        else:
            return None

class WithdrawManager(BalanceManager):
    def withdraw(self, acno, amount):
        current_balance = self.check_balance(acno)
        if current_balance is not None:
            new_balance = max(0, current_balance - amount)
            self.cur.execute("UPDATE customer SET balance = ? WHERE accno = ?;", (new_balance, acno))
            self.conn.commit()
            return True
        else:
            return False

class DepositManager(BalanceManager):
    def deposit(self, acno, amount):
        current_balance = self.check_balance(acno)
        if current_balance is not None:
            new_balance = current_balance + amount
            self.cur.execute("UPDATE customer SET balance = ? WHERE accno = ?;", (new_balance, acno))
            self.conn.commit()
            return True
        else:
            return False

class AccountManager:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.balance_manager = BalanceManager()
        self.withdraw_manager = WithdrawManager()
        self.deposit_manager = DepositManager()

    def create_account(self, name, accno, pin, balance):
        self.db_manager.cur.execute("INSERT INTO customer(name, accno, pin, balance) VALUES (?, ?, ?, ?);", (name, accno, pin, balance))
        self.db_manager.conn.commit()

    def verify_pin(self, pin):
        self.db_manager.cur.execute("SELECT accno FROM customer WHERE pin = ?;", (pin,))
        res = self.db_manager.cur.fetchone()
        return res[0] if res else None

def main():
    account_manager = AccountManager()

    print("\t\t\tWelcome to our bank")
    print("\n1. New account\n2. Existing account")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        name = input("Name: ")
        accno = int(input("Account Number: "))
        pin = int(input("PIN: "))
        balance = int(input("Balance: "))
        account_manager.create_account(name, accno, pin, balance)
        print("{} ,your account is created successfully!".format(name))

    elif choice == 2:
        acno = int(input("Enter account no.: "))
        pin = int(input("Enter your pin: "))
        verified_acno = account_manager.verify_pin(pin)
        if verified_acno == acno:
            print("\n\nOur bank welcomes you!")
            print("\n\n\t1. Balance ")
            print("\t2. Withdraw ")
            print("\t3. Deposit ")
            print("\t4. Exit ")
            c = int(input("\nEnter your choice: "))
            if c == 1:
                balance = account_manager.balance_manager.check_balance(acno)
                current_datetime = datetime.datetime.now()
                formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                print("\nFormatted Date and Time:", formatted_datetime)
                print("Your current account balance is rupees {} only".format(balance))
            elif c == 2:
                amount = int(input("Enter the amount to be withdrawn: "))
                if account_manager.withdraw_manager.withdraw(acno, amount):
                    print("Amount withdrawn successfully")
                    balance = account_manager.balance_manager.check_balance(acno)
                    current_datetime = datetime.datetime.now()
                    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    print("\nFormatted Date and Time:", formatted_datetime)
                    print("Your current account balance is rupees {} only".format(balance))
    
                else:
                    print("Failed to withdraw amount. Please check your account details.")
            elif c == 3:
                amount = int(input("Enter the amount to be deposited: "))
                if account_manager.deposit_manager.deposit(acno, amount):
                    print("Amount deposited successfully")
                    balance = account_manager.balance_manager.check_balance(acno)
                    current_datetime = datetime.datetime.now()
                    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    print("\nFormatted Date and Time:", formatted_datetime)
                    print("Your current account balance is rupees {} only".format(balance))
                else:
                    print("Failed to deposit amount. Please check your account details.")
            else:
                print("Invalid input")
                exit()
                


        else:
            print("Invalid PIN. Please try again.")
    else:
        print("Invalid input")
        exit()

    account_manager.db_manager.close_connection()

if __name__ == "__main__":
    main()
