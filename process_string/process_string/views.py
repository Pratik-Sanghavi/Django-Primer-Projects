from django.shortcuts import render
from json import dumps
import random

def VoweltoUpper(inp):
    vowels = 'aeiou'
    out = ''
    for char in inp:
        if char in vowels:
            out+=char.upper()
        else:
            out+=char.lower()
    return out
    
def reverse(s):
    out=''
    for i in reversed(range(len(s))):
        out+=s[i]
    return out

def RevWord(inp):
	# two pointer approach:
    # have two pointers point to the first and last letter before a space occurs
    # reverse that particular word and move on till the end of the string
    p1=0
    p2=0
    output=''
    while (p2<len(inp)):
        while(p2<len(inp) and inp[p2]!=' '):
            p2=p2+1
        output+=reverse(inp[p1:p2])
        p1=p2
        while(p1<len(inp) and inp[p1]==' '):
            output+=inp[p1]
            p1=p1+1
        p2=p1
	
    return output

def SortWord(inp):
	# two pointer approach:
    # have two pointers point to the first and last letter before a space occurs
    # sort that particular word and move on till the end of the string
    p1=0
    p2=0
    output=''
    while (p2<len(inp)):
        while(p2<len(inp) and inp[p2]!=' '):
            p2=p2+1
        output+=''.join(sorted(inp[p1:p2]))
        p1=p2
        while(p1<len(inp) and inp[p1]==' '):
            output+=inp[p1]
            p1=p1+1
        p2=p1
	
    return output

def DupRem(inp):
    # python strings cannot be modified after creation!!!
    # cannot use an inplace algorithm
    list=[]
    out=''
    for char in inp:
        if char not in list or char ==' ':
            list.append(char)
            out+=char
    return out

def NextChar(inp):
    out=''
    for char in inp:
        if char>='A' and char<='Z':
            newletter = ord('A')+(ord(char)+1-ord('A'))%26
            out+=(chr(newletter))
        elif char>='a' and char<='z':
            newletter = ord('a')+(ord(char)+1-ord('a'))%26
            out+=(chr(newletter))
        else:
            out+=(char)
    return out
def Encrypt(inp):
    key = random.randint(0,9)
    out = ''
    for char in inp:
        out+=chr(ord(char)^key)
    out+=str(key)
    return out

def Decrypt(inp):
    key = int(inp[-1])
    out=''
    for char in inp:
        out+=chr(ord(char)^key)
    return out[0:-1]

dict = {}
output =''

def home_view(request):
    global dict
    dict = request.GET #stores data entered by user in a dictionary
    return render(request, 'home.html')

def operation(request):
    global dict
    global output
    inp = dict['textinp']
    operation = int(dict['operation'])
    print(operation)
    if(operation==1):
        output = VoweltoUpper(inp)
    elif (operation==2):
        output = RevWord(inp)
    elif (operation==3):
        output = SortWord(inp)
    elif (operation==4):
        output = DupRem(inp)
    elif (operation==5):
        output = NextChar(inp)
    elif(operation==6):
        output = Encrypt(inp)
    if operation==6:
        op=output[0:-1]
    else:
        op=output
    return render(request, 'operation.html',{"Input": inp,"Output":op, "Opcode": dict['operation']})

def reverseop(request):
    inp = dict['textinp']
    print(output)
    decrypt = Decrypt(output)
    return render(request, 'reverseop.html',{"Input": inp,"Output":output, "Decrypt": decrypt})