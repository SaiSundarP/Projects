import tkinter as tk 
from tkinter import messagebox 
import datetime
import sqlite3

conn=sqlite3.connect("bank_records.db")
cur=conn.cursor()
def create():
      cur.execute("""CREATE TABLE customer(
                  name varchar(40) not null,
                  accno int unique,
                  pin smallint not null,
                  balance bigint );""")

   

def new_user():
        def submit():
                # Retrieve the values entered by the user
                name_val = name.get()
                accno_val = accno.get()
                pin_val = pin.get()
                balance_val = balance.get()

                # Basic validation
                if not name_val or not accno_val or not pin_val or not balance_val:
                    messagebox.showerror("Input Error", "All fields are required!")
                    return
        
                try:
                    accno_val = int(accno_val)
                    pin_val = int(pin_val)
                    balance_val = float(balance_val)  # Assuming balance could be a float
                except ValueError:
                    messagebox.showerror("Input Error", "Account Number, PIN, and Balance must be numeric!")
                    return

                try:
                # Insert the data into the database
                    cur.execute(
                    "INSERT INTO customer (name, accno, pin, balance) VALUES (?, ?, ?, ?);",
                    (name_val, accno_val, pin_val, balance_val))
                    conn.commit()
            
                # Provide feedback to the user
                    result_label.config(text="")
                    result_label.config(text=f"{name_val}, your account is created successfully!", fg="green",bg="lightblue",pady=10)
                    

                except sqlite3.IntegrityError as e:
                    messagebox.showerror("Database Error", f"Account creation failed: {e}")

                
                   
        name_label = tk.Label(root, text="Please enter your name:",bg="lightblue")
        name_label.pack()
        name=tk.Entry(root)
        name.pack()
        accno_label =tk.Label(root,text="Account Number: ",bg="lightblue")
        accno_label.pack()
        accno=tk.Entry(root)
        accno.pack()
        pin_label = tk.Label(root,text="PIN: ",bg="lightblue")
        pin_label.pack()
        pin=tk.Entry(root)
        pin.pack()
        balance_label = tk.Label(root,text="Balance: ",bg="lightblue")
        balance_label.pack()
        balance=tk.Entry(root)
        balance.pack()
        submit_button = tk.Button(root, text="Create Account", command= submit,cursor ="hand2",bg="lightgreen")
        submit_button.pack(pady=20)
        
        global result_label
        result_label = tk.Label(root, text="",bg="lightblue")
        result_label.pack()

        
           


def existing():
        def submit():
                global accno_val,pin_val,verified_acno
                accno_val = accno.get()
                pin_val = pin.get()
                
                # Basic validation
                if   not accno_val or not pin_val :
                    messagebox.showerror("Input Error", "All fields are required!")
                    return
        
                try:
                    accno_val= int(accno_val)
                    pin_val= int(pin_val)
                     
                except ValueError:
                    messagebox.showerror("Input Error","Account Number and PIN must be numeric!")
                    return

                try:
                    verified_acno = verify_pin(pin_val)
                    if verified_acno == accno_val:
                        accno_label.config(text="")
                        accno.pack_forget()
                        pin_label.config(text="")
                        pin.pack_forget()
                        submit_button.pack_forget()
                        next()
                    
                    else:
                          messagebox.showerror("Database Error","Account no and PIN does not match")
                         
        
                except sqlite3.IntegrityError as e :
                    messagebox.showerror("Database Error", f"Sorry failed to fetch your details: {e}")
                  
                  
       
        
        accno_label =tk.Label(root,text="Account Number: ",bg="lightblue")
        accno_label.pack()
        accno=tk.Entry(root)
        accno.pack()

        pin_label = tk.Label(root,text="PIN: ",bg="lightblue")
        pin_label.pack()
        pin=tk.Entry(root)
        pin.pack()
        
        submit_button = tk.Button(root, text="Enter", command= submit,cursor ="hand2",bg="lightgreen")
        submit_button.pack(pady=20)
        
#function to withdraw
def withdraw(acno):
        def submit():
            amount_val=amount.get()
            try:
                amount_val=int(amount_val)
            except ValueError :
                 messagebox.showerror("Input Error","Amount must be in numeric!")
            try:
                current_balance = check_balance(acno)
                if current_balance is not None:
                    result_label.config(text="")
                    amount_label.config(text="")
                    amount.pack_forget()
                    submit_button.pack_forget()
                    new_balance = max(0, current_balance - amount_val)
                    cur.execute("UPDATE customer SET balance = ? WHERE accno = ?;", (new_balance, acno))
                    conn.commit()
                    result_label.config(text="",bg="lightblue")
                    result_label.config(text=f"Rs.{amount_val} withdrawn successfully!",fg="green",bg="lightblue")
                   
            
                else:
                    messagebox.showerror("Database Error","Opertion failed due to insufficient money!")
            except sqlite3.IntegrityError as e:
                    messagebox.showerror("Database Error", f"Withdrawal operation failed: {e}")
        amount_label=tk.Label(root,text="Enter Amount :",bg="lightblue")
        amount_label.pack()
        amount=tk.Entry()
        amount.pack()
        submit_button = tk.Button(root, text="Enter", command= submit,cursor ="hand2",bg="lightgreen")
        submit_button.pack(pady=20)
        result_label = tk.Label(root, text="",bg="lightblue")
        result_label.pack()
        


#function to deposit amount
def deposit(acno):
        global result_label,amount_label,amount,submit_button
        def submit():
            amount_val=amount.get()
            try:
                amount_val=int(amount_val)
            except ValueError :
                 messagebox.showerror("Input Error","Amount must be in numeric!")
            try:
                current_balance = check_balance(acno)
                if current_balance is not None:
                    result_label.config(text="")
                    amount_label.config(text="")
                    amount.pack_forget()
                    submit_button.pack_forget()
                    new_balance = max(0, current_balance + amount_val)
                    cur.execute("UPDATE customer SET balance = ? WHERE accno = ?;", (new_balance, acno))
                    conn.commit()
                    result_label.config(text="")
                    result_label.config(text=f"Rs.{amount_val} deposited successfully!",fg="green",bg="lightblue")
                   
            
                else:
                    messagebox.showerror("Database Error","Opertion failed due to insufficient money!")
            except sqlite3.IntegrityError as e:
                    messagebox.showerror("Database Error", f"Deposit operation failed: {e}")
        
        amount_label=tk.Label(root,text="Enter Amount :",bg="lightblue")
        amount_label.pack()
        amount=tk.Entry()
        amount.pack()
        submit_button = tk.Button(root, text="Enter", command= submit,cursor ="hand2",bg="lightcoral")
        submit_button.pack(pady=20)
        result_label = tk.Label(root, text="",bg="lightblue")
        result_label.pack()
        
       
def check_balance(acno):
        cur.execute("SELECT balance FROM customer WHERE accno = ?;", (acno,))
        res = cur.fetchone()
        if res:
             return res[0] if res else None

     
#function to check balance
def balance(acno):
        
        cur.execute("SELECT balance FROM customer WHERE accno = ?;", (acno,))
        res = cur.fetchone()
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
        if res:
            result_label=tk.Label(text=f"\nFormatted Date and Time: {formatted_datetime} \nYour current account balance is rupees {res[0]} only",bg="lightblue")
            result_label.pack()
        else:
            return None
        
        

#function to verify pin       
def verify_pin(pin):
        cur.execute("SELECT accno FROM customer WHERE pin = ?;", (pin,))
        res = cur.fetchone()
        return res[0] if res else None

#creates two choices
def choice():
    tk.Button(buttonframe,text="Existing User",width=15,command =lambda:existing(),fg="blue",bg="yellow",cursor="hand2").grid(row=0,column=0,padx=10 )
    tk.Button(buttonframe,text="New User",width=15,command=lambda:new_user(),fg="blue",bg="yellow",cursor="hand2").grid(row=0,column=1,padx=10)
    tk.Button(buttonframe,text="Exit",width=15,command =lambda:exit(),fg="blue",bg="yellow",cursor="hand2").grid(row=0,column=2,padx=10)
#creates buttons for withdraw,deposit,balance
def next():
   
    tk.Button(buttonframe,text="Withdraw",width=15,command =lambda:withdraw(accno_val),fg="blue",bg="yellow",cursor="hand2").grid(row=0,column=0,padx=10 )
    tk.Button(buttonframe,text="Deposit",width=15,command=lambda:deposit(accno_val),fg="blue",bg="yellow",cursor="hand2").grid(row=0,column=1,padx=10)
    tk.Button(buttonframe,text="Balance",width=15,command =lambda:balance(accno_val),fg="blue",bg="yellow",cursor="hand2").grid(row=0,column=2,padx=10 )
    tk.Button(buttonframe,text="Exit",width=15,command =lambda:exit(),fg="blue",bg="yellow",cursor="hand2").grid(row=0,column=3,padx=10)


#main function creates user interface window
def main():
    global buttonframe,root
    root=tk.Tk()
    root.title("ATM INTERFACE")
    root.geometry("500x300")
    root.configure(bg="lightblue")
    

    result_label=tk.Label(root,text="Welcome to our Bank",bg="lightblue",font=("Calibri",15))
    result_label.pack(pady=10)

    buttonframe=tk.Frame(root)
    buttonframe.pack(pady=20)
    if sqlite3.OperationalError is True:
       create()

    choice()
    root.mainloop()

if __name__=="__main__":
     main()
