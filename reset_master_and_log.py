import os
import time
import pandas as pd

print("Warning - This will reset the log files. Enter Y/N ")
choice=input()
if choice=="Y":
    print("Deleting log files")
    path="Market Activity Report 2020"
    folders=os.listdir(path)
    for i in folders:
        print(".",end="")
        if i!="All ZIP":
            temp_path=os.path.join(path,i)
            temp=os.listdir(temp_path)
            if "log.txt" in temp:
                os.remove(os.path.join(temp_path,"log.txt"))
    print()
    print("Deleted all log files")
print("Warning - This will reset the current master.csv. Enter Y/N ")
#choice = input()
if choice=="Y":
    try:
        temp=pd.read_csv("header.csv")
        temp.to_csv("master.csv",index=False)
        print("New empty master.csv created successfully!")
        time.sleep(3)
    except PermissionError:
        print("???????????????????????????????????")
        print("Failed to create new empty master.csv\nclose master.csv and try again")
        time.sleep(3)
