import os 
import json
import sys

CHANGED_FILES = os.environ.get("CHANGED_FILES")
CURRENT_USER = os.environ.get("CURRENT_USER")
ALLOWED_USERS = os.environ.get("ALLOWED_USERS")

allowedUsersReadable = json.loads(ALLOWED_USERS)

#Checken ob CURRENT_USER Administrator ist. Falls ja, alle Aenderungen erlauben
for user in allowedUsersReadable["administrators"]:
    if user == CURRENT_USER:
        print("Welcome Administrator!")
        sys.exit(0)

        
#Wenn keine Aenderungen erkannt werden, bzw. eine Aenderung 1:1 rueckgaengig gemacht wurde, 
#ist der Test gueltig
if CHANGED_FILES == "":
    print("No changes detected.")
    sys.exit(0)

#Der erste oberste Pfad wird als einzige gueltige Firma anerkannt
#Existiert diese nicht, oder aeandert sie sich innerhalb eines Pull Requests, ist der Test ungueltig
currentCompany = CHANGED_FILES.split()[0].split('/')[0]

#Checken, ob in nur einem Pfad Aenderungen vorgenommen wurden
for file in CHANGED_FILES.split():
    if currentCompany == file.split('/')[0]:
        pass
    else:
        print('::error::You are not allowed to make changes in multiple directories!')
        sys.exit(1)

#Checken ob CURRENT_USER für currentCompany zugelassen ist
try:
    for i in range(len(allowedUsersReadable)):
        if allowedUsersReadable[currentCompany]:
            for user in allowedUsersReadable[currentCompany]:
                if user == CURRENT_USER:
                    print("User is valid!")
                    sys.exit(0)
                    
except (KeyError):
    print('::error::You are not allowed, to make changes in this directory!')
    sys.exit(1) 


print('::error::You are not allowed, to make changes in this directory!')
sys.exit(1) 
