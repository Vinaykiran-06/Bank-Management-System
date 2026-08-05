from datetime import datetime
import json

class BankAccount:
    
    def __init__(self,owner,balance,account_no,pin,is_new=True):
        self.owner=owner
        self.balance=balance
        self.account_no=account_no
        self.__pin=pin
        self.transactions=[]
        
        if is_new:
            self.add_transaction("account opened", balance)
        
    def __str__(self):
        return f"""
    Account Holder : {self.owner}
    Account Balance : ₹{self.balance}
    Account Number : {self.account_no}
    
    """
    
    def deposit(self,amount,pin):
        if not self.verify_pin(pin):
            return "Invalid pin"
        if amount > 0: 
            self.balance+=amount
            self.add_transaction("Deposit" , amount)
            return f"Available balance: {self.balance}"
        else:
            return "Invalid deposit amount"
        
    def withdraw(self,amount,pin):
        if not self.verify_pin(pin):
            return "invalid pin"
        if amount <= self.balance and amount > 0:
            self.balance-=amount
            self.add_transaction("Withdrawn", amount)
            return f"Available balance: {self.balance}"
        else:
            return "Invalid amount or Insufficient amount"
        
    def check_balance(self,pin):
        if not self.verify_pin(pin):
            return"Invalid pin"
            
        return f" Available balance: {self.balance}"
    
    def show_transactions(self,pin):
        if not self.verify_pin(pin):
            return "Invalid pin "
        print("\n transaction history")
        for transaction in self.transactions:
            print("-----------------------------")
            print("Type: ", transaction["type"])
            print("Amount: ", transaction["amount"])
            print("Date: ", transaction["date"])
            
    def add_transaction(self,transaction_type,amount):
        transaction={
            "type" : transaction_type,
            "amount" : amount,
            "date" : datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
        self.transactions.append(transaction)
        
    def transfer(self,receiver,amount):
        if amount<=self.balance and amount >0:
            self.balance-=amount
            receiver.balance+=amount
            self.add_transaction("transfer sent to " + receiver.owner , amount)
            receiver.add_transaction("transfer received from " +self.owner, amount)
            return "Transfer sucessful"
        else:
            return "Invalid amount or insufficient balance"
    
    def verify_pin(self,pin):
        return self.__pin==pin

    
class Bank:
    def __init__(self):
        self.accounts=[]
        self.account_no = 1000
    def create_account(self):
        
        name=input("Enter your name: ")
        balance=int(input("Enter your initial balance "))
        pin=int(input("create your pin : "))
        
        self.account_no += 1
        account_no = self.account_no
        
        account=BankAccount(name,balance,account_no,pin)
        self.accounts.append(account)
        
        print("Account created sucessfully")
        
    def find_account(self):
        account_number=int(input("Enter account number: "))
        for account in self.accounts:
            if account.account_no == account_number :
                return account
        return None
    
    def save_data(self):
        data=[]
        for account in self.accounts:
            account_data={
            "owner": account.owner,
            "balance": account.balance,
            "account_no": account.account_no,
            "pin": account._BankAccount__pin,
            "transactions": account.transactions                
            }
            data.append(account_data)
            
        with open("accounts.json","w") as file:
            json.dump(data,file,indent=4)
        print("Data saved successfully")
            
    def load_data(self):
        try:
            
            with open("accounts.json","r") as file:
                data=json.load(file)
                for account_data in data:
                    account=BankAccount(
                        account_data["owner"],
                        account_data["balance"],
                        account_data["account_no"],
                        account_data["pin"],
                        is_new=False
                    )
                    account.transactions = account_data["transactions"]
                    self.accounts.append(account) 
            if self.accounts:
                self.account_no=max(account.account_no for account in self.accounts)   
        except FileNotFoundError:
            return    
bank = Bank()
bank.load_data()  

while True:
    print("\n===== BANK MANAGEMENT SYSTEM =====")
    
    print("\nchoose your option: ")
    print("""
1.create account
2.deposit
3.withdraw
4.check balance
5.transaction history
6.exit""")
    
    choice=int(input("Enter your choice: "))
    
    if choice == 1:
        bank.create_account()
    elif choice == 2:

        account = bank.find_account()
        if account:
            pin=int(input("Enter PIN: "))
            dep_amount=float(input("enter amount: "))
            print(account.deposit(dep_amount,pin))
        else:
            print("Account not found")
        
        
        
    elif choice == 3:
        account = bank.find_account()
        
        if account:
            with_amount=float(input("enter amount: "))
            pin = int(input("enter pin: "))
            print(account.withdraw(with_amount,pin))
        else:
            print("Invalid account")
            
    elif choice == 4:
        account = bank.find_account()
        if account:
            pin=int(input("Enter PIN: "))
            print(account.check_balance(pin))
        else:
            print("Account not found")
    
    elif choice==5:
        account = bank.find_account()
        
        if account:
            pin=int(input("Enter PIN: "))
            account.show_transactions(pin)
        else:
            print("Account not found")
    
    elif choice == 6:
        bank.save_data()
        print("Thank you")
        break
    else :
        print("Tnvalid choice")
    
    
