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
            return SQLfunctions.GetPersonID(self)
        

    
    class Transaction:
        def __init__(self, date_id, transactionMoney, person_id, location):
            self.date_id = date_id
            self.transactionMoney = transactionMoney
            self.person_id = person_id
            self.location = location
		
        def StartTransaction(self, purchasedItems, person):
            id = int(SQLfunctions.StartTransaction(self))  #Returns transaction ID
            for item in purchasedItems:
                SQLfunctions.InsertItem(id, item)
            SQLfunctions.UpdateTransactions(id)
            SQLfunctions.updateMoneySpent(person.GetPersonID(), id)
        
        def CheckTransactions(self, date):
            print(SQLfunctions.CheckTransactions(self, date))


    class PurchasedItems:
        def __init__(self, item, price, quantity):
            self.item = item
            self.price = price
            self.quantity = quantity
    
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
        Date = Timetable(InputDate())
        Date.InsertDate()
        User = InputUser()
        user = person(User, 0, 0)
        user.insertToDB()
        items = InputPurchasedItems()
        transactionLocation = InputTransactionLocation()
        transaction = Transaction(Date.GetDateID(), 0, user.GetPersonID(), transactionLocation)
        transaction.StartTransaction(items, user)
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
            input = Input("Enter item purchased in parentheses () and Base Price and Quanity(Type exitNOW once you are done!)\n")
            if input.lower() == "exitnow":
                break
            items = re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+', input)
            itemName = items[0].strip("()")
            itemPrice = int(items[1])
            try:
                itemQuantity = float(items[2])
            except IndexError:
                itemQuantity = 1
                
            item = PurchasedItems(itemName, itemPrice, itemQuantity)
            inputs.append(item)
        return inputs
    
    def InputTransactionLocation():
        return Input("Enter where you made this transaction\n")
        

    main()