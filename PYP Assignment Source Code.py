#TP063418 Ken Nara Gazza
import datetime

#SYSTEM OVERVIEW
#Banking system works with four file types
#Database file
#   Record containing account count and all account IDs
#   First line contains the number of registered accounts (superuser, admin, active customers, inactive customers)
#   Second line contains superuser ID
#   Third line contains admin IDs
#   Fourth line contains active customerIDs
#   Fifth line contains inactive customerIDs
#Superuser file
#   Contains the superuser's account details and account changes history
#   First line of the file contains account details (userID and password)
#   Succeeding lines contains the history of changes made to other accounts such as admin account creation
#Admin file
#   Contains the admin's account details and account changes history
#   First line of the file contains account details (userID and password)
#   Succeeding lines contains the history of changes made to other accounts such as customer account creation and customer password changes of the customer account
#Customer file
#   Contains the customer's account details, account balances, and transaction and password change history
#   First line of the file contains account details (userID and password), balances (current and savings), and account status (inactive and active)
#   Second line contains the credentials of the owner of the account
#   Succeeding lines contain the transaction history and password change history of the customer account
#Each user registered into the system is represented by a file labelled with the user ID
#There are three types of user IDs
#   Superuser user ID starts with 'superuser'
#   Admin user IDs start with 'admin'
#   Customer user IDs start with 'customer'
#User ID and password are automatically generated via timestamp

#Converts a list with sublists into a single string
def listToString(listOfList):
    newList = []
    for subList in listOfList:
       #subList is converted in a string and appended into newList
       itemString = "#".join(subList)
       newList.append(itemString)
    #newList is converted into a string
    newListString = "\n".join(newList)
    return newListString

#Converts a single string into a list with sublist
def stringToList(string):
    newList = []
    #String is seperated at \n into items within list
    list = string.split("\n")
    for item in list:
        #Each item in list is seperated at # into items within subList and subList is append into newList
        subList = item.split("#")
        newList.append(subList)
    return newList

#Reads the contents of a file with the name filename into a list. Returns that if the file is found and None if not file is found
def fileReader(filename):
    try:
        #Reads contents of file into filedata and returns filedata
        file = open(filename, "r")
        fileContents = file.read()
        file.close
        fileData = stringToList(fileContents)
        return fileData
    except FileNotFoundError:
        print("File not found!")
    except:
        print("Exception occured!")
    
#Writes data within fileData into a file with the name filename. Returns None
def fileWriter(filename, fileData):
    try:
        fileContents = listToString(fileData)
        file = open(filename, "w")
        file.write(fileContents)
        file.close
    except FileNotFoundError:
        print("File not found!")
    except:
        print("Exception occured!")

#superUserInitializer creates a superuser file. Returns none
def superUserIntializer(superUserId):
    superUserAccountData = []
    creationDate = datetime.datetime.now()
    passwordTimestamp = creationDate.timestamp()
    superUserPassword = str(round(passwordTimestamp, 2))
    accountCredentials = [superUserId, superUserPassword]
    superUserAccountData.append(accountCredentials)
    fileWriter(superUserId, superUserAccountData)
    print(f"A superuser account has been created with the user id {superUserId} and password {superUserPassword}")

#fileDatabaseInitializer creates a database file with the registered superuser account. Returns None
def fileDatabaseInitializer(fileDatabaseId, superUserId):
    fileDatabaseAccountData = []
    accountCount = ["1", "0", "0", "0", "0"]
    fileDatabaseAccountData.append(accountCount)
    superUserIdList = ["superUserIds" ,superUserId]
    fileDatabaseAccountData.append(superUserIdList)
    adminIdList = ["adminIds"]
    fileDatabaseAccountData.append(adminIdList)
    activeCustomerIdList = ["activeCustomerIds"]
    fileDatabaseAccountData.append(activeCustomerIdList)
    inactiveCustomerIdList = ["inactiveCustomerIds"]
    fileDatabaseAccountData.append(inactiveCustomerIdList)
    fileWriter(fileDatabaseId, fileDatabaseAccountData)

#Creates superuser and filedatabase files if none are found. Returns None
def programInitializer():
    superUserId = "superuser1"
    fileDatabaseId = "fileDatabase"
    while True:
        superUser = fileReader("superuser1")
        fileDatabase = fileReader("fileDatabase")
        if superUser == None:
            superUserIntializer(superUserId)
            continue
        elif fileDatabase == None:
            fileDatabaseInitializer(fileDatabaseId, superUserId)
            continue
        else:
            break

def customerAccountDataInitializer():
    fileDatabase = fileReader("fileDatabase")
    userData = []
    totalCustomerCount = int(fileDatabase[0][4])
    customerNumberId = str(totalCustomerCount + 1)
    customerId = "customer" + customerNumberId
    customerAccountData = [customerId, "null", "null", "null", "inactive"]
    userData.append(customerAccountData)
    return userData

def getCustomerCredentials(userData):
    userCredentials = []
    firstName = str(input("Enter your first name: "))
    userCredentials.append(firstName)
    lastName = str(input("Enter you last name or (None) if you have no last name: "))
    userCredentials.append(lastName)
    age = int(input("Enter your age: "))
    if age < 18:
        print("You need to be at least 18 to open a bank account!")
        return False
    else:
        userCredentials.append(str(age))
        nationalId = str(input("Enter your national ID: "))
        userCredentials.append(nationalId)
        homeAddress = str(input("Enter your home address: "))
        userCredentials.append(homeAddress)
        phoneNumber = str(input("Enter your phone number: "))
        userCredentials.append(phoneNumber)
        email = str(input("Enter your email: "))
        userCredentials.append(email)
        userData.append(userCredentials)
        return userData

#Registration function to initially create an inactive customer account which can be activated by an admin. Returns None
def registrationForm():
    #Initial customer account data creation to be append into the first line of the file
    userData = customerAccountDataInitializer()
    #Prompting user to enter their credentials to be appended into the second line of the file
    userData = getCustomerCredentials(userData)
    if userData == False:
        return False
    else:
        customerId = userData[0][0]
        accountCountUpdater(0,0,1,1)
        customerIdUpdater(customerId, "inactive")
        print(f"A temporary customer account with a user ID {customerId} has been created. Please wait for admin staff to verify account.")
        return userData

#Login function which prompts the user to enter the user ID and password to enter their account. Returns the user data of the account if the login is successful and None if login is cancelled or if the user completed registration
def login():
    while True:
        userId = str(input("Enter your user ID or (1) to cancel the login and (2) to register for a customer account: "))
        if userId == "1":
            print("Login has been cancelled.")
            break
        if userId == "2":
            userData = registrationForm()
            if userData != None:
                filename = userData[0][0]
                fileWriter(filename, userData)
                continue
            else:
                continue
        elif userId != None:
            userData = fileReader(userId)
            if userData != None:
                accountId = userData[0][0]
                if "customer" in accountId:
                    userStatus = userData[0][4]
                    if userStatus == "inactive":
                        print("This account has not been activated! Please wait for the admin staff to activated this account. Contact the admin staff should you have any further inquiries.")
                        break
                    else:
                        credentialLock = passwordVerification(userData)
                        if credentialLock == True:
                            print("Welcome User")
                            return userData
                        else:
                            continue
                else:
                   credentialLock = passwordVerification(userData)
                   if credentialLock == True:
                       print("Welcome User")
                       return userData
                   else:
                       continue
            else:
                print("Incorrect User ID!")
                continue
        else:
            continue  

#passwordVerification function prompts the user to enter their password. Returns True if the password is correct and False if the password is incorrect or the verification is cancelled
def passwordVerification(userData):
    password = userData[0][1]
    inputPassword = str(input("Enter your password or (1) to cancel: "))
    if inputPassword == password:
        return True
    elif inputPassword == "1":
        print("Verification has been cancelled.")
        return False
    else:
        print("Password is incorrect!")
        return False

def withdrawFromCurrent(userData):
    currentBalance = int(userData[0][2])
    if currentBalance == 500:
        print("Your current balance has reached the minimum amount. Please deposit in order to withdraw.")
        return userData
    else:
        withdrawalAmount = int(input("Enter the withdrawal amount: RM"))
        credentialLock = passwordVerification(userData)
        if credentialLock == True:
            newCurrentBalance = currentBalance - withdrawalAmount
            if newCurrentBalance < 500:
                print("Transaction failed! You've withdrawn over the minimum balance. Your balance will not be updated.")
                return userData
            else:
                print(f"Transaction successful! You've withdrawn RM{withdrawalAmount} from your current account. Your new balance is RM{newCurrentBalance}.")
                userData[0][2] = str(newCurrentBalance)
                userData = transactionHistoryUpdater(userData,"current", "withdraw", str(withdrawalAmount))
                return userData
        else:
            return userData

def withdrawFromSavings(userData):
    savingsBalance = int(userData[0][3])
    if savingsBalance == 100:
        print("Your savings balance has reached the minimum amount. Please deposit in order to withdraw.")
        return userData
    else:
        withdrawalAmount = int(input("Enter the withdrawal amount: RM"))
        credentialLock = passwordVerification(userData)
        if credentialLock == True:
            newSavingsBalance = savingsBalance - withdrawalAmount
            if newSavingsBalance < 100:
                print("Transaction failed! You've withdrawn over the minimum balance. Your balance will not be updated.")
                return userData
            else:
                print(f"Transaction successful! You've withdrawn RM{withdrawalAmount} from your savings account. Your new balance is RM{newSavingsBalance}.")
                userData[0][3] = str(newSavingsBalance)
                userData = transactionHistoryUpdater(userData,"savings", "withdraw", str(withdrawalAmount))
                return userData
        else:
            return userData

def depositToCurrent(userData):
    currentBalance = int(userData[0][2])
    depositAmount = int(input("Enter a deposit amount: RM"))
    credentialLock = passwordVerification(userData)
    if credentialLock == True:
        newCurrentBalance = currentBalance + depositAmount
        print(f"Transaction successful! You've deposited RM{depositAmount} to your current account. Your new balance is RM{newCurrentBalance}.")
        userData[0][2] = str(newCurrentBalance)
        userData = transactionHistoryUpdater(userData, "current", "deposit", str(depositAmount))
        return userData
    else:
        return userData

def depositToSavings(userData):
    savingsBalance = int(userData[0][3])
    depositAmount = int(input("Enter a deposit amount: "))
    credentialLock = passwordVerification(userData)
    if credentialLock == True:
        newSavingsBalance = savingsBalance + depositAmount
        print(f"Transaction successful! You've deposited RM{depositAmount} to your current account. Your new balance is RM{newSavingsBalance}.")
        userData[0][3] = str(newSavingsBalance)
        newUserData = transactionHistoryUpdater(userData, "savings", "deposit", str(depositAmount))
        return newUserData
    else:
        return userData

#transactionHistoryUpdater function updates the customer account history log with a transaction log. Returns userData
def transactionHistoryUpdater(userData, accountType, transactionType, transactionAmount):
    dateOfTransaction = datetime.datetime.now()
    dateLog = dateOfTransaction.strftime("%d-%B-%Y %H:%M:%S")
    transactionLog = [transactionType, dateLog, accountType, transactionAmount]
    userData.append(transactionLog)
    return userData

#customerPasswordChanger function changes the password of the customer account. Returns userData
def customerPasswordChanger(userData):
    credentialLock = passwordVerification(userData)
    if credentialLock == True:
        while True:
            inputPassword = str(input("Enter your new password or (1) to cancel: "))
            if inputPassword == "1":
                print("Password change has been cancelled!")
                return userData
            else:
                confirmInputPassword = str(input("Confirm your new password: "))
                if confirmInputPassword == inputPassword:
                    print("Your password has been updated!")
                    userData[0][1] = inputPassword
                    dateOfPasswordChange = datetime.datetime.now()
                    dateLog = dateOfPasswordChange.strftime("%d-%B-%Y %H:%M:%S")
                    passwordChangeHistoryLog = ["passwordChange", dateLog]
                    userData.append(passwordChangeHistoryLog)
                    return userData
                else:
                    print("Password does not match!")
                    continue
    else:
        print("Incorrect password! If you need help to change your current password please contact Admin staff.")
        return userData

#adminHistoryUpdater function updates the admin account history log with an action log. Returns adminUserData
def adminHistoryUpdater(adminUserData, userData, adminAction):
    userId = userData[0][0]
    dateOfAdminAction = datetime.datetime.now()
    dateLog = dateOfAdminAction.strftime("%d-%B-%Y %H:%M:%S")
    adminActionLog = [adminAction, dateLog, userId]
    adminUserData.append(adminActionLog)
    print("pee pee poo poo")
    return adminUserData

#adminPasswordChanger function allows admin user to change the password of a selected customer account. Returns adminUserData
def adminCustomerPasswordChanger(adminUserData, customerId):
    customerUserData = fileReader(customerId)
    while True:
        newPassword = str(input("Enter the new password: "))
        confirmNewPassword = str(input("Confirm the new password: "))
        if confirmNewPassword == newPassword:
            print(f"{customerId}'s password has been updated.")
            customerUserData[0][1] = newPassword
            fileWriter(customerId, customerUserData)
            adminUserData = adminHistoryUpdater(adminUserData, customerUserData, "changeCustomerPassword")
            return adminUserData
        else:
            print("Password is incorrect! Please try again")
            continue

#accountCountUpdater function updates the current count of the accounts registered in the system. Returns None
def accountCountUpdater(adminCountIncrement, activeCustomerCountIncrement, inactiveCustomerCountIncrement, totalCustomerIncrement):
    fileDatabase = fileReader("fileDatabase")
    adminCount = int(fileDatabase[0][1])
    activeCustomerCount = int(fileDatabase[0][2])
    inactiveCustomerCount = int(fileDatabase[0][3])
    totalCustomerCount = int(fileDatabase[0][4])
    newAdminCount = str(adminCount + adminCountIncrement)
    fileDatabase[0][1] = newAdminCount
    newActiveCustomerCount = str(activeCustomerCount + activeCustomerCountIncrement)
    fileDatabase[0][2] = newActiveCustomerCount
    newInactiveCustomerCount = str(inactiveCustomerCount + inactiveCustomerCountIncrement)
    fileDatabase[0][3] = newInactiveCustomerCount
    newTotalCustomerCount = str(totalCustomerCount + totalCustomerIncrement)
    fileDatabase[0][4] = newTotalCustomerCount
    fileWriter("fileDatabase", fileDatabase)

def adminIdUpdater(accountId):
    fileDatabase = fileReader("fileDatabase")
    adminUserIds = fileDatabase[2]
    adminUserIds.append(accountId)
    fileDatabase[2] = adminUserIds
    fileWriter("fileDatabase", fileDatabase)

def customerIdUpdater(accountId, accountStatus):
    fileDatabase = fileReader("fileDatabase")
    activeCustomerIds = fileDatabase[3]
    inactiveCustomerIds = fileDatabase[4]
    if accountStatus == "active":
        activeCustomerIds.append(accountId)
        fileDatabase[3] = activeCustomerIds
        try:
            inactiveCustomerIds.remove(accountId)
            fileDatabase[4] = inactiveCustomerIds
            fileWriter("fileDatabase", fileDatabase)
        except:
            fileWriter("fileDatabase", fileDatabase)
    elif accountStatus == "inactive":
        inactiveCustomerIds.append(accountId)
        fileDatabase[4] = inactiveCustomerIds
        try:
            activeCustomerIds.remove(accountId)
            fileDatabase[3] = activeCustomerIds
            fileWriter("fileDatabase", fileDatabase)
        except:
            fileWriter("fileDatabase", fileDatabase)

def initialCustomerActivator(adminUserData, customerAccountData):
    while True:
        startingSavingsBalance = int(input("Enter the starting savings account balance: "))
        if startingSavingsBalance < 100:
            print("Invalid input! The starting savings balance cannot be less than RM100!")
            continue
        else:
            startingCurrentBalance = int(input("Enter the starting current account balance: "))
            if startingCurrentBalance < 500:
                print("Invalid input! The starting current balance cannot be less than RM500.")
                continue
            else:
                creationDate = datetime.datetime.now()
                passwordTimestamp = creationDate.timestamp()
                customerPassword = str(round(passwordTimestamp, 2))
                inputFinalActivationChoice = str(input("Enter (1) to confirm balance inputs and finish account initialization, (2) to reinput balances, or (3) to cancel activation: "))
                if inputFinalActivationChoice == "1":
                    customerAccountData[0][1] = customerPassword
                    customerAccountData[0][2] = str(startingCurrentBalance)
                    customerAccountData[0][3] = str(startingSavingsBalance)
                    customerAccountData[0][4] = "active"
                    customerId = customerAccountData[0][0]
                    fileWriter(customerId, customerAccountData)
                    customerIdUpdater(customerId, "active")
                    accountCountUpdater(0,1,-1,0)
                    adminUserData = adminHistoryUpdater(adminUserData, customerAccountData, "intializedCustomerAccount")
                    print(f"{customerId} was successfully initialized!")
                    return adminUserData
                elif inputFinalActivationChoice == "2":
                    continue
                elif inputFinalActivationChoice == "3":
                    print("Account activation has been cancelled.")
                    return adminUserData

def customerReactivator(adminUserData, customerAccountData):
    customerAccountData[0][4] == "active"
    customerId = customerAccountData[0][0]
    customerIdUpdater(customerId, "active")
    accountCountUpdater(0,1,-1,0)
    adminUserData = adminHistoryUpdater(adminUserData, customerAccountData, "reactivatedCustomerAccount")
    print("Account has been activated")
    return adminUserData

#customerActivator function allows admin to activate a customer account with the user ID customerId. Returns adminUserData
def customerActivator(adminUserData, customerId):
    customerAccountData = fileReader(customerId)
    customerDetails = customerAccountData[1]
    inputActivationChoice = str(input(f"This is the registration details of {customerId}: {customerDetails} \nEnter (1) to initialize the account, (2) to reactivate the account, and (3) to cancel activation and return to the main menu: "))
    if inputActivationChoice == "1":
        adminUserData = initialCustomerActivator(adminUserData, customerAccountData)
        return adminUserData
    elif inputActivationChoice == "2":
        adminUserData = customerReactivator(adminUserData, customerAccountData)
        return adminUserData
    elif inputActivationChoice == "3":
        print("Account activation has been cancelled.")
        return adminUserData

#customerDeactivator function allows admin to deactivate a customer account with the user ID customerId. Returns adminUserData
def customerDeactivator(adminUserData, customerId):
    customerAccount = fileReader(customerId)
    inputDeactivationChoice = str(input(f"Enter (1) to deactivate {customerId} or (2) to return to the main menu: "))
    if inputDeactivationChoice == "1":
        customerAccount[0][4] == "inactive"
        customerIdUpdater(customerId, "inactive")
        accountCountUpdater(0,-1,1,0)
        adminUserData = adminHistoryUpdater(adminUserData, customerAccount, "deactivatedCustomerAccount")
        print("Account has been deactivated")
        return adminUserData
    elif inputDeactivationChoice == "2":
        print("Account deactivation has been cancelled.")
        return adminUserData

#adminAccountCreator function creates an admin account and updates superUserData. Returns superUserData
def adminAccountCreator(superUserData):
    adminFileData = []
    adminCredentials = []
    fileDatabase = fileReader("fileDatabase")
    adminAccountCount = int(fileDatabase[0][1])
    adminAccountIds = fileDatabase[2]
    adminNumberId = str(adminAccountCount + 1)
    adminId = "admin" + adminNumberId
    adminCredentials.append(adminId)
    adminAccountIds.append(adminId)
    fileDatabase[2] = adminAccountIds
    creationDate = datetime.datetime.now()
    passwordTimestamp = creationDate.timestamp()
    adminPassword = str(round(passwordTimestamp, 2))
    adminCredentials.append(adminPassword)
    adminFileData.append(adminCredentials)
    accountCountUpdater(1,0,0,0)
    adminIdUpdater(adminId)
    fileWriter(adminId, adminFileData)
    superUserData = adminHistoryUpdater(superUserData, adminFileData, "createdAdminAccount")
    print(f"Admin account with user ID {adminId} and password {adminPassword} has been created.")
    return superUserData

#customerAccountHistoryViewer function displays the specified history log. Returns None
def customerAccountHistoryViewer(userData, historyType):
    if historyType == "transaction":
       for sublist in userData:
            if "withdraw" in sublist:
                print(sublist)
            elif "deposit" in sublist:
                print(sublist)
            else: 
                continue
    elif historyType == "password":
        for sublist in userData:
            if "passwordChange" in sublist:
                print(sublist)
            else:
                continue

#adminAccountHistoryViewer function prints out the history log of an admin user or the superuser. Returns None
def adminAccountHistoryViewer(adminUserData):
    for sublist in adminUserData:
        if "createdAdminAccount" in sublist:
            print(sublist)
        elif "initializedCustomerAccount" in sublist:
            print(sublist)
        elif "deactivatedCustomerAccount" in sublist:
            print(sublist)
        elif "reactivatedCustomerAccount" in sublist:
            print(sublist)

def superUserMenu(superUserData):
    while True:
        fileDatabase = fileReader("fileDatabase")
        inputAccount = str(input("Enter (1) to create an admin account, (2) to view the total number of accounts, (3) to view account history, or (4) to exit the main menu: "))
        if inputAccount == "1":
            superUserData = adminAccountCreator(superUserData)
            continue
        elif inputAccount == "2":
            adminAccountCount = fileDatabase[0][1]
            adminAccountIds = fileDatabase[2]
            print(f"There are {adminAccountCount} admin accounts of which are: {adminAccountIds}")
            totalCustomerCount = fileDatabase[0][4]
            activeCustomerCount = fileDatabase[0][2]
            inactiveCustomerCount = fileDatabase[0][3]
            activeCustomerIds = fileDatabase[3]
            inactiveCustomerIds = fileDatabase[4]
            print(f"There are {totalCustomerCount} total customer accounts of which {activeCustomerCount} are active and {inactiveCustomerCount} are inactive which are: {activeCustomerIds} {inactiveCustomerIds} respectively.")
            continue
        elif inputAccount == "3":
            adminAccountHistoryViewer(superUserData)
            continue
        elif inputAccount == "4":
            print("You have exited the main menu.")
            superUserId = superUserData[0][0]
            fileWriter(superUserId, superUserData)
            break

def adminMenu(adminUserData):
    while True:
        fileDatabase = fileReader("fileDatabase")
        inputAccount = str(input("Enter (1) to view unactivated customer accounts, (2) to view activated customer accounts, (3) to change the password of a customer account, (4) to view change history, or (5) to exit the main menu: "))
        if inputAccount == "1":
            inactiveCustomerCount = fileDatabase[0][3]
            inactiveCustomerIds = fileDatabase[4]
            inputAction = str(input(f"There are currently {inactiveCustomerCount} inactive customer accounts which are: {inactiveCustomerIds} \nEnter the customer ID to verify or reactivate (1) return to the main menu: "))  
            if inputAction in inactiveCustomerIds:
                adminUserData = customerActivator(adminUserData, inputAction)
                continue
            elif inputAction == "1":
                print("You have returned to the main menu.")
                continue
            else:
                print("Invalid input was entered! Please try again.")
                continue
        elif inputAccount == "2":
            activeCustomerCount = fileDatabase[0][2]
            activeCustomerIds = fileDatabase[3]
            inputAction = str(input(f"There are currently {activeCustomerCount} active customer accounts which are: {activeCustomerIds} \nEnter the customer ID to deactivate or (1) to return to the main menu: "))
            if inputAction in activeCustomerIds:
                adminUserData = customerDeactivator(adminUserData, inputAction)
                continue
            elif inputAction == "1":
                print("You have returned to the main menu.")
                continue
            else:
                print("Invalid input was entered! Please try again.")
                continue
        elif inputAccount == "3":
            inputAction = str(input(f"Enter the user ID of the customer account or (1) to return to the main menu: "))
            if inputAction in activeCustomerIds:
                adminUserData = adminCustomerPasswordChanger(adminUserData, inputAction)
                continue
            elif inputAction == "1":
                print("You have returned to the main menu.")
                continue
            else:
                print("Invalid input was entered! Please try again.")
                continue
        elif inputAccount == "4":
            adminAccountHistoryViewer(adminUserData)
            continue
        elif inputAccount == "5":
            print("You have exited the main menu.")
            adminId = adminUserData[0][0]
            fileWriter(adminId, adminUserData)
            break

def customerMenu(userData):
    while True:
        inputAccount = str(input("Enter (1) to access your current account, (2) to access your savings account, (3) to change passwords, (4) to view transaction history, (5) to view account change history, or (6) to exit the main menu: "))
        if inputAccount == "1":
            currentBalance = userData[0][2]
            inputTransaction = str(input(f"Your current account balance is: {currentBalance} \nEnter (1) to withdraw from this account, (2) to deposit to this account, or (3) to return to the main menu: "))
            if inputTransaction == "1":
                userData = withdrawFromCurrent(userData)
                continue
            elif inputTransaction == "2":
                userData = depositToCurrent(userData)
                continue
            elif inputTransaction == "3":
                print("TYou have returned to the main menu.")
                continue
        elif inputAccount == "2":
            savingsBalance = userData[0][3]
            inputTransaction = str(input(f"Your savings account balance is: {savingsBalance} \nEnter (1) to withdraw from this account, (2) to deposit to this account, or (3) to return to the main menu: "))
            if inputTransaction == "1":
                userData = withdrawFromSavings(userData)
                continue
            elif inputTransaction == "2":
                userData = depositToSavings(userData)
                continue
            elif inputTransaction == "3":
                print("You have returned to the main menu.")
                continue
        elif inputAccount == "3":
            userData = customerPasswordChanger(userData)
            continue
        elif inputAccount == "4":
            customerAccountHistoryViewer(userData, "transaction")
            continue
        elif inputAccount == "5":
            customerAccountHistoryViewer(userData, "password")
            continue
        elif inputAccount == "6":
            print("You have exit the main menu.")
            filename = userData[0][0]
            fileWriter(filename, userData)
            break

def menu(userData):
    userId = userData[0][0]
    if "customer" in userId:
        customerMenu(userData)
    elif "admin" in userId:
        adminMenu(userData)
    elif "superuser" in userId:
        superUserMenu(userData)

def main():
    programInitializer()
    while True:
        userData = login()
        if userData == None:
            continue
        else:
            menu(userData)
            continue

main()