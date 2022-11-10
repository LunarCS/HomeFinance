import SQLfunctions
from datetime import date, datetime
import re

#TODO: Allow db to read current date, insert date into timetable, utizlie date id in transaction and other stuff



if __name__ == "__main__":
    

    
    class person:
        def __init__(self, name, moneySpent, moneyGained):
            self.name = name
            self.moneySpent = moneySpent
            self.moneyGained = moneyGained
        
        def insertToDB(self):
            SQLfunctions.insertPerson(self)
        
        def updateMoneySpent(self, transaction):
            SQLfunctions.updateMoneySpent(self, transaction)
        
        def gainMoney(self, Income):
            SQLfunctions.updateGainedMoney(self, Income)
        
        def GetPersonID(self):
            return SQLfunctions.GetPersonID(person)
        

    
    class Transaction:
        def __init__(self, date_id, transactionMoney, person_id, location):
            self.date_id = date_id
            self.transactionMoney = transactionMoney
            self.person_id = person_id
            self.location = location
		
        def StartTransaction(self, purchasedItems):
            id = int(SQLfunctions.StartTransaction(self))  #Returns transaction ID
            for item in purchasedItems:
                SQLfunctions.InsertItem(id, item)
            SQLfunctions.UpdateTransactions(self)
        
        def CheckTransactions(self, date):
            print(SQLfunctions.CheckTransactions(self, date))


    class PurchasedItems:
        def __init__(self, item, price):
            self.item = item
            self.price = price
    
    class Income:
        def __init__(self, moneyGained):
            self.moneyGained = moneyGained
    class Timetable:
        def __init__(self,date=date.today()):
            self.date = date
        
        def GetDateID(self):
            return SQLfunctions.GetDateID(self.date)
        
        def InsertDate(self):
            SQLfunctions.InsertDate(self)
        
    
    def main(): 
        SQLfunctions.c.execute("SELECT * FROM People")
        Date = Timetable(InputDate())
        Date.InsertDate()
        User = InputUser()
        user = person(User, 0, 0)
        user.insertToDB()
        items = InputPurchasedItems()
        transaction = Transaction(Date.GetDateID(), 0, user.GetPersonID(), InputTransactionLocation())
        transaction.StartTransaction(items)
        return
    
    def Input(message):
        return input(message).capitalize()
    
    def InputDate():
        format = "%Y-%m-%d"
        Date = Input("Enter transaction date (YYYY-MM-DAY), (If transaction was done today just type today)\n").split('-')

        if Date[0].lower() != "today":
            Date = '-'.join(Date)
        else:
            Date = date.today()
        while not ValidateFormat(format, Date):
            InputDate()
        else:
            return Date
        

    def ValidateFormat(format, Date):
        try:
            datetime.strptime(Date, format)
            validation = True
        except:
            validation = False
            print("Incorrect format. Date must be YYYY-MM-DD")
        finally:
            return validation
    def InputUser():
        return Input("Enter username NO SPACES\n")
    
    def InputIncome():
        return Input("Enter your income\n")
    
    def InputPurchasedItems():
        inputs = []
        while (True):
            input = Input("Enter item purchased in parentheses () and Price (Type exitNOW once you are done!)\n")
            if input == "exitNOW":
                break
            items = re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+', input)
            itemName = items[0].strip("()")
            itemPrice = items[1]
            item = PurchasedItems(itemName, itemPrice)
            inputs.append(item)

            
        return 
    
    def InputTransactionLocation():
        return Input("Enter where you made this transaction\n")
        

    main()