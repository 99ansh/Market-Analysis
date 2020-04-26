import pandas as pd
import os
import datetime
import warnings
warnings.filterwarnings("ignore")
try: 
    os.rename('master.csv', 'tempmaster.csv')
    os.rename('tempmaster.csv', 'master.csv')
    
    path="Market Activity Report 2020"
    del_folders=["fo23042020"]
    temp=pd.read_csv("master.csv")
    temp_dates=[]
    for i in del_folders:
        temp_path=os.path.join(path,i)
        if "log.txt" in os.listdir(temp_path):
            os.remove(os.path.join(temp_path,"log.txt"))
            print(i+" log deleted")
        date=i[2:]
        year=int(date[-4:])
        month=int(date[2:4])
        day=int(date[:2])
        temp_dates.append(datetime.date(year,month,day).strftime("%d/%m/%Y"))
    ct=0
    for i in temp_dates:
        x=temp["date"]==i
        temp.drop(temp[temp["date"]==i].index,inplace=True)
        ct+=x.sum()
    temp.to_csv("master.csv",index=False)
    print("Total number of rows deleted",ct)

except OSError:
    print('master.csv or tempmaster.csv is still open. Close it and try again')
