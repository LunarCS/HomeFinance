from sqlite3 import connect

conn = connect("DailyTransactions.db", isolation_level=None)
c = conn.cursor()

def convertTuple(tup):
        # initialize an empty string
    string = ''
    for item in tup:
        string = string + str(item) + "*"
    return string

#Person functions

def insertPerson(person):
    try:
        c.execute("""INSERT INTO People (Name, TotalMoneyGained, TotalMoneySpent)
        VALUES (:name, 0, 0)""", {'name': person.name})
    except:
        print("User is already in database!")

def updateMoneySpent(person, transaction):
    c.execute("""
    UPDATE People
    SET TotalMoneySpent = TotalMoneySpent + 
    (SELECT TransactionMoney
    FROM Transactions
    WHERE person_id == :personID
    AND TransactionID == :transactionId)
    """, {'person_id':GetPersonID(person.name), 'transactionID':GetTransactionID(person.name)})

def updateGainedMoney(person, Income, date):
    personID = GetPersonID(person.name)
    c.execute("""INSERT INTO Income
    VALUES(:date_id, :person_id, :moneyGained)""", {'date_id':GetDateID(date), 'person_id':personID, 'moneyGained': Income.moneyGained})
    c.execute("""
    UPDATE People
    SET TotalMoneyGained = TotalMoneyGained + (
        SELECT SUM(moneyGained)
        FROM Income
        WHERE person_id == :personID)
    """, {'personID':personID})

#Transaction functions

def InsertItem(transactionid, purchasedItem):
    c.execute("""
    INSERT INTO PurchasedItems
    VALUES (:transaction_id, :item, :price)""", {'transaction_id':transactionid, 'item':purchasedItem.item, 'price':purchasedItem.price})

def StartTransaction(transaction, person):
    c.execute("""
    INSERT INTO Transactions (date_id, TransactionMoney, person_id, TransactionLocation)
    VALUES (:date_id, 0, :person_id, :location)""",
    {'date_id':transaction.date_id, 'person_id':GetPersonID(person.name), 'location':transaction.location})

    c.execute("""
    SELECT TransactionID
    FROM Transactions
    ORDER BY DESC
    LIMIT 1""")
    return int(convertTuple(c.fetchone()).split('*'))


def UpdateTransactions(transaction):
    c.execute("""
    UPDATE Transactions
    SET TransactionMoney = :totalPrice
    )
    """, {'totalPrice': TotalPrice(transaction)})

def CheckTransactions(transaction, date):
    ids = GetTransactionID(date, transaction.location)
    idArray = []
    for id in ids:
        id = int(convertTuple(id).strip("*"))
        if id not in idArray:
            idArray.append(id)
    print(idArray)
    placeholders= ', '.join(['?']*len(idArray))
    c.execute("""
    SELECT Date, TransactionMoney, TransactionLocation
    FROM Transactions
    JOIN Timetable ON date_id = DateID
    WHERE TransactionID IN ({})""".format(placeholders), idArray)
    return c.fetchall()

#Item functions

def TotalPrice(id):
    c.execute("""
        (SELECT SUM(Price)
        FROM PurchasedItems
        WHERE transaction_id == :transaction_id)""", {'transaction_id':id})
    return int(convertTuple(c.fetchone()).split('*'))

#Timetable functions

def InsertDate(date):
    try:
        c.execute("""
        INSERT INTO Timetable (Date)
        VALUES (:date)""", {'date':date.date})
    except:
        return

#Get IDs
def GetDateID(date):
    c.execute("""
    SELECT dateID
    FROM Timetable
    WHERE Date == :date""", {'date':date})
    return int(convertTuple(c.fetchone()).split('*'))

def GetPersonID(person):
    c.execute("""
    SELECT PersonID
    FROM People
    WHERE Name == :name""", {'name':person.name})
    return int(convertTuple(c.fetchone()).split('*'))

def GetTransactionID(date, location):
    c.execute("""
    SELECT TransactionID
    FROM Transactions
    WHERE date_id == (
        SELECT DateID
        FROM Timetable
        WHERE Date == :date)
    AND TransactionLocation == :location""", {'date':date, 'location':location})
    return c.fetchall()




#def getTransactionid()
#def getPersonid()

def DeleteAll():
    c.execute("DELETE FROM PurchasedItems")
    c.execute("DELETE FROM Transactions")
    c.execute("DELETE FROM People")
    c.execute("DELETE FROM Timetable")

