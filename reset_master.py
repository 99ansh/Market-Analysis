import pandas as pd
import time
print("Warning - This will reset the current master.csv. Enter Y/N ")
choice = input()
try:
    if choice=="Y":
        temp=pd.read_csv("header.csv")
        temp.to_csv("master.csv",index=False)
        print("New empty master.csv created successfully!")
        time.sleep(3)
except PermissionError:
    print("???????????????????????????????????")
    print("Failed to create new empty master.csv\nclose master.csv and try again")
    time.sleep(5)
