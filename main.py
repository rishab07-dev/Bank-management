import random
import string
import json
from pathlib import Path

#first project in python Bank management system


class Bank:
    database='data.json'
    data=[]
    try:
        if Path(database).exists():#checking if the file exists or not
            with open(database, "r") as fs:
               data=json.load(fs)  # opening the json file and loading the data into a variable
        else:
            print("File not found")
    except Exception as e:
        print(f"Error occurred while loading data: {e}")

    @classmethod
    def __update(cls):
        with open(cls.database, "w") as fs:
            fs.write(json.dumps(Bank.data))#dumping the data into the json file

            
    @classmethod
    def __account_number(cls):
        alpha = random.choices(string.ascii_letters,k = 3)
        num = random.choices(string.digits,k= 3)
        spchar = random.choices("!@#$%^&*",k = 1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)



    def createaccount(self):
        info={ #defining the data structure for the account
            "name":input("Enter your name: "),
            "age":int(input("Enter your age: ")),
            "email":input("Enter your email: "),
            "pin":int(input("Enter your pin: ")),
            "account_number":Bank.__account_number(),
            "balance":0
        }
        if info['age'] < 18 or len(str(info['pin']))!=4:
            print("You are not eligible to create an account")
        else:
            print("Account created successfully") 
            for i in info:
                print(f"{i}: {info[i]}")
        print("note down your account number for future reference")  


        Bank.data.append(info)
        Bank.__update()

    def withdraw(self):
        account_number=input("Enter your account number: ")
        pin=int(input("Enter your pin: "))
        userdata=[i for i in Bank.data if i['account_number']==account_number and i['pin']==pin]# checking if the account number and pin are correct
        
        if userdata == False:
            print("Account number or pin is incorrect")
        else:
            amount=int(input("Enter the amount to be withdrawn: "))
            if userdata[0]['balqnce'] < amount:
                print("You account balance is less than the amount you want to withdraw")
            else:
                userdata[0]['balance'] -= amount #dummy data amount added to the balance
                Bank.__update()#updating the data in the json file
                print(f"Amount withdrawn successfully. Your new balance is {userdata[0]['balance']}")
        
        


    def deposit(self):
        account_number=input("Enter your account number: ")
        pin=int(input("Enter your pin: "))
        userdata=[i for i in Bank.data if i['account_number']==account_number and i['pin']==pin]# checking if the account number and pin are correct

        if userdata == False:
            print("Account number or pin is incorrect")
        else:
            amount=int(input("Enter the amount to be deposited: "))
            if amount >10000 or amount < 0:
                print("You can only deposit between 0 to 10000")
            else:
                userdata[0]['balance'] += amount #dummy data amount added to the balance
                Bank.__update()#updating the data in the json file
                print(f"Amount deposited successfully. Your new balance is {userdata[0]['balance']}")


    def checkbalance(self):
        account_number=input("Enter your account number: ")
        pin=int(input("Enter your pin: "))
        userdata=[i for i in Bank.data if i['account_number']==account_number and i['pin']==pin]# checking if the account number and pin are correct
        print(f"Your information is:\n\n")
        for i in userdata[0]:
            print(f"{i}: {userdata[0][i]}")


    def updateaccount(self):
        account_number=input("Enter your account number: ")
        pin=int(input("Enter your pin: "))
        userdata=[i for i in Bank.data if i['account_number']==account_number and i['pin']==pin]# checking if the account number and pin are correct
        if userdata == False:
            print("Account number or pin is incorrect")
        else:
            print("what do you want to update?\n1. Name\n2. Email\n3. Pin")
            new_data={
                "name":input("Enter your new name or enter to skip: "),
                "email":input("Enter your new email or enter to skip: "),
                "pin":(input("Enter your new pin or enter to skip: "))
            }#creating a new data structure for the updated data
        if new_data['name']=="":
            new_data['name']=userdata[0]['name']
        if new_data['email']=="":
            new_data['email']=userdata[0]['email']
        if new_data['pin']=="":
            new_data['pin']=userdata[0]['pin']
        new_data['age']=userdata[0]['age']
        new_data['account_number']=userdata[0]['account_number']
        new_data['balance']=userdata[0]['balance']
        if type(new_data['pin'])==str:
            new_data['pin']=int(new_data['pin'])#converting the pin to int if it is a string
        for i in new_data:
            if new_data[i]==userdata[0][i]:
                continue
            else:
                userdata[0][i]=new_data[i]#updating the data in the json file
        Bank.__update()
        print("Account updated successfully")

    def deleteaccount(self):
        account_number=input("Enter your account number: ")
        pin=int(input("Enter your pin: "))
        userdata=[i for i in Bank.data if i['account_number']==account_number and i['pin']==pin]# checking if the account number and pin are correct
        if userdata == False:
            print("Account number or pin is incorrect")
        else:
            check=input("Are you sure you want to delete your account? (y/n): ")
            if check=="n" or check=="N":
                pass
            else:
                index=Bank.data.index(userdata[0])#getting the index of the user data in the list
                Bank.data.pop(index)#removing the user data from the list\
                print("Account deleted successfully")
                Bank.__update()#updating the data in the json file


obj=Bank()

print("press 1 for creating a account")
print("press 2 for depositing money")
print("press 3 for withdrawing money")
print("press 4 for checking balance")
print("press 5 for update account details")
print("press 6 for deleting account")

n=int(input("Enter your choice: "))
if n==1:
    obj.createaccount()
if n==2:
    obj.deposit()
if n==3:
    obj.withdraw()
if n==4:
    obj.checkbalance()
if n==5:
    obj.updateaccount()
if n==6:
    obj.deleteaccount()