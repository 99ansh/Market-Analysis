import os
import time
print("Warning - This will reset the log files. Enter Y/N ")
choice=input()
try:
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
    time.sleep(3)
except PermissionError:
    print("???????????????????????????????????")
    print("Failed to delete log.txt in "+i+"\nclose log.txt and try again")
    time.sleep(5)
