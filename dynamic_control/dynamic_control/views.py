from django.shortcuts import render
from json import dumps
import numpy as np
from json import dumps
from datetime import datetime

dict_hw = {}
dict_dd = {}
drop_list=[]
Y1=0
Y2=0
count=0
queuelog=[]

def alphastring(x):
    for i in x:
        if(i.isalpha()==False and i!="\n" and i!=' '):
            return False
    return True

def numstring(x):
    for i in x:
        if(i.isnumeric()==False and i!="\n"):
            return False
    return True

def alnumstring(x):
    for i in x:
        if(i.isalnum()==False and i!="\n"):
            return False
    return True

def home_view(request):
    global dict_hw
    global dict_hw
    global dict_dd
    global drop_list
    global Y1
    global Y2
    dict_hw = {}
    dict_dd = {}
    drop_list=[]
    Y1=0
    Y2=0
    dict_hw = request.GET #stores data entered by user in a dictionary
    if(len(dict_hw)==0):
        return render(request, 'home.html')
    return render(request, 'home.html',{'Number' : int(dict_hw['number']),'Columns' : int(dict_hw['columns'])})

def drop_down(request):
    global dict_hw
    global dict_dd
    global drop_list
    global Y1
    global Y2
    num = int(dict_hw['number'])
    if(len(dict_dd)==0):
        drop_list.append(((200*np.random.rand(1,num))+1).astype(int).tolist())
        Y1 = ((6*np.random.rand(1,num))+1).astype(int).tolist()
        Y2 = ((3*np.random.rand(1,num))+1).astype(int).tolist()
    JSONdrop_list = dumps(drop_list[0])
    dict_dd=request.GET
    if(len(dict_dd)==0):
        return render(request, 'drop_down.html',{'Droplist':JSONdrop_list,'Number' : num,'Columns' : int(dict_hw['columns']),'i':1})
    selection = int(dict_dd['drop_select'])
    return render(request, 'drop_down.html',{'Droplist':JSONdrop_list,'Number' : num,'Columns' : int(dict_hw['columns']),'i':selection+1,'Option':drop_list[0][0][selection],'Y1':Y1[0][selection],'Y2':Y2[0][selection]})

def show_result(request):
    global dict_hw
    global dict_dd
    global drop_list
    global Y1
    global Y2
    global count
    global queuelog
    selection = int(dict_dd['drop_select'])
    cont = Y1[0][selection]
    datatype = Y2[0][selection]
    now=datetime.now()
    label=[]
    with open('data.txt','r') as f:
        data=f.readlines()
        i=0
        for x in data:
            if (i>=drop_list[0][0][selection]):
                break
            if(datatype==1):
                if(alphastring(x)):
                    label.append(x)
                    i=i+1

            elif (datatype==2):
                if (numstring(x)):
                    label.append(x)
                    i=i+1

            if(datatype==3):
                if (alnumstring(x)):
                    label.append(x)
                    i=i+1

    with open('log.txt','w') as f:
        count=count+1
        if(len(queuelog)==5):
            queuelog = queuelog[1:]
        queuelog.append(str(count)+'\t'+str(selection)+'\t'+str(cont)+'\t'+str(datatype)+'\t'+str(label)+'\t'+str(now)+"\n")
        for log in queuelog:
            f.write(log)
    JSONdrop_list = dumps(drop_list)
    JSONlabel = dumps(label)
    columns = int(dict_hw['columns'])
    return render(request, 'show_result.html',{'Droplist':JSONdrop_list,'Number' : int(dict_hw['number']),'i':selection+1,'Option':drop_list[0][0][selection],'Columns':columns,'Y1':cont,'Labels':JSONlabel,'Datatype':datatype})