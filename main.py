import pandas as pd
import os
import datetime
import csv
import time
import warnings
warnings.filterwarnings("ignore")
d1={'SYMBOL':'SYMBOL','EXP_DATE':'EXPIRY','STR_PRICE':'STRIKE PRICE','OPT_TYPE':'OPTION TYPE', 'OPEN_PRICE':'OPEN PRICE', 'HI_PRICE':'HI PRICE',
    'LO_PRICE':'LO PRICE', 'CLOSE_PRICE':'CLOSE PRICE', 'PERCENT_CHG':'%' ,'OPEN_INT*':'OPEN INTEREST','DATE':'DATE' ,'OPEN_PRICEX':'F & O OPEN' ,
    'HI_PRICEX':'F & O HI', 'LO_PRICEX':'F & O LO','CLOSE_PRICEX':'F & O CLOSE'}
d2={'SYMBOL':'SYMBOL','EXPIRY':'EXP_DATE','STRIKE PRICE':'STR_PRICE','OPTION TYPE':'OPT_TYPE','OPEN PRICE':'OPEN_PRICE', 'HI PRICE':'HI_PRICE',
    'LO PRICE':'LO_PRICE', 'CLOSE PRICE':'CLOSE_PRICE','%':'PERCENT_CHG' ,'OPEN INTEREST':'OPEN_INT*','DATE':'DATE' ,'F & O OPEN':'OPEN_PRICEX',
    'F & O HI':'HI_PRICEX', 'F & O LO':'LO_PRICEX','F & O CLOSE':'CLOSE_PRICEX'}

#try: 
os.rename('master.csv', 'tempmaster.csv')
os.rename('tempmaster.csv', 'master.csv')

path="Market Activity Report 2020"
folders=os.listdir(path)    
temp_dates=[]
for i in ["fo03012020","fo06012020","fo01012020","fo07012020"]:
#for i in folders:
    if i!="All ZIP":
        temp_folder=i
        print("UPDATING DATA FROM "+i)
        date=temp_folder[2:]
        year=int(date[-4:])
        month=int(date[2:4])
        day=int(date[:2])
        #date_format=datetime.date(year,month,day).strftime("%d-%m-%y")
        file1="op"+date+".csv"
        file2="fo"+date+".csv"
        file3="log.txt"
        status=False
        if file3 not in os.listdir(os.path.join(path,temp_folder)):
            
            status=True
            df1=pd.read_csv(os.path.join(path,temp_folder,file1))
            df2=pd.read_csv(os.path.join(path,temp_folder,file2))
            df1.drop(df1.index[-1],inplace=True)
            df2.drop(df2.index[-1],inplace=True)
            col={}
            for i in df1.columns.values:
                col[i]=i.rstrip()
            df1.rename(columns=col,inplace=True)
            col={}
            for i in df2.columns.values:
                col[i]=i.rstrip()
            
            df2.rename(columns=col,inplace=True)

            df2=df2[['SYMBOL', 'EXP_DATE', 'OPEN_PRICE', 'HI_PRICE','LO_PRICE', 'CLOSE_PRICE']]
            
            temp_dates.append(datetime.date(year,month,day).strftime("%d/%b/%Y"))
            df1["DATE"]=[datetime.date(year,month,day).strftime("%d/%b/%Y") for i in range(df1.shape[0])]
            df1["OPEN_PRICEX"]=""
            df1["HI_PRICEX"]=""
            df1["LO_PRICEX"]=""
            df1["CLOSE_PRICEX"]=""
            
            for i in range(df1.shape[0]):
                year=int(df1.EXP_DATE[i][6:])
                #print(year)
                month=int(df1.EXP_DATE[i][3:5])
                day=int(df1.EXP_DATE[i][0:2])
                df1.EXP_DATE[i]=datetime.date(year,month,day).strftime("%d/%b/%Y")
            
            for i in range(df2.shape[0]):
                year=int(df2.EXP_DATE[i][6:])
                #print(year)
                month=int(df2.EXP_DATE[i][3:5])
                day=int(df2.EXP_DATE[i][0:2])
                df2.EXP_DATE[i]=datetime.date(year,month,day).strftime("%d/%b/%Y")
            

            df2["month"]=[df2.EXP_DATE[i][3:6] for i in range(df2.shape[0])]

            df1["time"]=[datetime.datetime.timestamp(datetime.datetime.strptime(df1.EXP_DATE[i],"%d/%b/%Y")) for i in range(df1.shape[0])]
            df1["time2"]=[datetime.datetime.timestamp(datetime.datetime.strptime(df1.DATE[i],"%d/%b/%Y")) for i in range(df1.shape[0])]
            df1["month"]=[df1.EXP_DATE[i][3:6] for i in range(df1.shape[0])]          
            for i in range(df2.shape[0]):
                df1.loc[(df1["SYMBOL"]==df2["SYMBOL"][i]) & (df1["month"]==df2["month"][i]),["OPEN_PRICEX","HI_PRICEX","LO_PRICEX","CLOSE_PRICEX"]]=df2["OPEN_PRICE"][i],df2["HI_PRICE"][i],df2["LO_PRICE"][i],df2["CLOSE_PRICE"][i]
            df1.drop(["INSTRUMENT",'TRD_QTY','NO_OF_CONT','NO_OF_TRADE','NOTION_VAL','PR_VAL'],axis=1,inplace=True)
        else:
            status=False
            f=open(os.path.join(path,temp_folder,file3),"r")
            print(temp_folder+" ALREADY "+f.read())
            f.close()
        if status==True:
            temp=pd.read_csv("master.csv")
            temp["time"]=""
            temp["month"]=""
            temp["time2"]=""
            #temp["PERCENT_CHG"]=""
            col={}
            for i in temp.columns.values:
                col[i]=i.rstrip()
            temp.rename(columns=col,inplace=True)
            temp.rename(columns=d2,inplace=True)
            temp["time"]=[datetime.datetime.timestamp(datetime.datetime.strptime(temp.EXP_DATE[i],"%d/%b/%Y")) for i in range(temp.shape[0])]
            temp["time2"]=[datetime.datetime.timestamp(datetime.datetime.strptime(temp.DATE[i],"%d/%b/%Y")) for i in range(temp.shape[0])]
            temp["month"]=[temp.EXP_DATE[i][3:5] for i in range(temp.shape[0])]
                
            temp=pd.concat([temp,df1],ignore_index=True)
            temp=temp.sort_values(["SYMBOL","time","EXP_DATE","STR_PRICE","OPT_TYPE","time2"],ascending=(True,True,True,True,True,True))
            temp.drop(["time","month","time2"],axis=1,inplace=True)
            '''
            for i in range(1,temp.shape[0]):
                if temp.STR_PRICE[i-1]==temp.STR_PRICE[i] and temp.OPT_TYPE[i-1]==temp.OPT_TYPE[i]:
                    print(i)
                    if temp.CLOSE_PRICE[i-1]==0:
                        if temp.CLOSE_PRICE[i-1]>0:
                            temp.PERCENT_CHG=999999999
                        elif temp.CLOSE_PRICE[i-1]<0:
                            temp.PERCENT_CHG=-999999999
                        else:
                            temp.PERCENT_CHG=0
                        print("DIVISION BY ZERO, UNEXPECTED MAY HAPPEN")
                    else:
                        temp.PERCENT_CHG[i]=((temp.CLOSE_PRICE[i]-temp.CLOSE_PRICE[i-1])*100)/temp.CLOSE_PRICE[i-1]
            '''
            temp.rename(columns=d1,inplace=True)
            temp.to_csv("master.csv",index=False)
            
            print("MASTER FILE UPDATED by ",temp_folder)
            print("---------------------------------------------------")
            f=open(os.path.join(path,temp_folder,file3),"w")
            f.write("completed"+" "+str(datetime.datetime.now()))
            f.close()
if len(temp_dates)>0:
    print("Calculating % % % % % % % for dates ",temp_dates)
    temp=pd.read_csv("master.csv")
    col={}
    for i in temp.columns.values:
        col[i]=i.rstrip()
    temp.rename(columns=col,inplace=True)
    temp.rename(columns=d2,inplace=True)
    temp["PERCENT_CHG"]=""
    for i in range(1,temp.shape[0]):
        if temp.DATE[i] in temp_dates:
            if temp.STR_PRICE[i-1]==temp.STR_PRICE[i] and temp.OPT_TYPE[i-1]==temp.OPT_TYPE[i]:
                #print(i)
                if temp.CLOSE_PRICE[i-1]==0:
                    if temp.CLOSE_PRICE[i-1]>0:
                        temp.PERCENT_CHG=999999999
                    elif temp.CLOSE_PRICE[i-1]<0:
                        temp.PERCENT_CHG=-999999999
                    else:
                        temp.PERCENT_CHG=0
                    print("DIVISION BY ZERO, UNEXPECTED MAY HAPPEN")
                else:
                    temp.PERCENT_CHG[i]=round(((temp.CLOSE_PRICE[i]-temp.CLOSE_PRICE[i-1])*100)/temp.CLOSE_PRICE[i-1],2)
    temp=temp[['SYMBOL','EXP_DATE' ,'STR_PRICE', 'OPT_TYPE', 'OPEN_PRICE', 'HI_PRICE',
     'LO_PRICE', 'CLOSE_PRICE', 'PERCENT_CHG' ,'OPEN_INT*','DATE' ,'OPEN_PRICEX' ,'HI_PRICEX', 'LO_PRICEX',
     'CLOSE_PRICEX']]
    temp.rename(columns=d1,inplace=True)
    '''
    ct=0
    l=['SYMBOL','EXP_DATE' ,'STR_PRICE', 'OPT_TYPE', 'OPEN_PRICE', 'HI_PRICE',
     'LO_PRICE', 'CLOSE_PRICE', 'PERCENT_CHG' ,'OPEN_INT*', 'TRD_QTY' ,'NO_OF_CONT' ,'NO_OF_TRADE',
     'NOTION_VAL', 'PR_VAL' ,'DATE' ,'OPEN_PRICEX' ,'HI_PRICEX', 'LO_PRICEX',
     'CLOSE_PRICEX']
    for i in range(1,temp.shape[0]):
        if ct==30:
            ct=0
            df1 = temp[0:i]
            df2 = temp[i:] 
            df1.loc[i]=l
            temp=pd.concat([df1,df2])
        ct+=1
    '''
    temp.to_csv("master.csv",index=False)
    print("THANK YOU")
    time.sleep(3)
else:
    print("Nothing found to update")
    print("THANK YOU")
    time.sleep(3)

#except OSError:
#    print('master.csv or tempmaster.csv is still open. Close it and try again')
