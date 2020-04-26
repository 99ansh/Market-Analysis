import os
import pandas as pd
import time
#move master.csv to old master
f=open("track_master.txt","r")
l=f.readlines()
last_v=l[-1]
f.close()

f=open("track_master.txt","w")
for i in range(1,int(last_v)+2):
    f.writelines(str(i)+"\n")
f.close()

new_path="Old Masters"
new_file="master"+str(int(last_v)+1)+".csv"
try:
    os.replace("master.csv",os.path.join(new_path,new_file))
    print("shifted master.csv to "+new_path+" "+new_file)
    temp=pd.read_csv("header.csv")
    temp.to_csv("master.csv",index=False)
    print("New empty master.csv created successfully")
    time.sleep(3)
except PermissionError:
    print("???????????????????????????????????")
    print("Failed to move master.csv\nclose master.csv and try again")
    time.sleep(5)
