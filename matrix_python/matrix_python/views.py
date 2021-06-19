from django.shortcuts import render
import numpy as np
from subprocess import run, PIPE
import time
from json import dumps

# declare global variables
dict = {} #stores user input
mat = [] #stores generated matrix
start = None   #stores start time
stop = None #stores end time
diff = None #stores time for execution


def home_view(request):
    global dict
    dict = request.GET #stores data entered by user in a dictionary
    return render(request, 'home.html') #creates the home.html page

def matrix(request):
    # declare global variables
    global start
    global stop
    global diff
    global mat
    #convert user inputs to appropriate data types
    rows = int(dict['rows'])
    columns = int(dict['columns'])
    bounds = dict['bounds']
    # split bounds on delimiter ','
    bounds = bounds.split(',')
    bounds[0] = int(bounds[0])
    bounds[1] = int(bounds[1])

    #if user doesn't need a unique valued matrix then :-
    if "unique" not in dict.keys():
        start = time.process_time()
        # map from 0,1 space to a,b space. Here a simple linear mapping is implemented.
        multiplicand = bounds[1]-bounds[0]
        mat = (np.round((multiplicand * np.random.rand(rows, columns))+bounds[0]))
        print('Matrix: ')
        # since matrix may be very large, string container may not be able to hold it. Therefore we pass it as a JSON object
        stringmat = dumps(mat.tolist())
        # some basic preprocessing to make our job of creation of table in the corresponding html file easier
        stringmat = stringmat.replace(',',' ')
        stringmat = stringmat.replace('.0',',')
        stringmat = stringmat.replace(',]',']')
        print(stringmat)
        stop = time.process_time()
    else:
        start = time.process_time()
        multiplicand = bounds[1]-bounds[0]
        mat = np.round((multiplicand * np.random.rand(rows, columns))+bounds[0])
        unique_dict = {i: i for i in range(bounds[0], bounds[1]+1)}
        nlist = []
        remnum = []
        
        # get indices of matrix containing repeated elements
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                if unique_dict[mat[i][j]] == mat[i][j]:
                    unique_dict[mat[i][j]] = 1
                else:
                    nlist.append([i, j])
        # get all elements in range that have not been used up in matrix
        for i in range(bounds[0], bounds[1]):
            if unique_dict[i] == i:
                remnum.append(i)
        # change the non-unique values to values remaining in the range (values not used up from range)
        # for this optimally we could randomly shuffle remnum and then run over the indices.
        # however since the non unique values themselves occur randomly, we can comfortably sequentially run over remnum without affecting the randomness 
        for k in range(len(nlist)):
            mat[nlist[k][0]][nlist[k][1]] = remnum[k]
        print('Matrix: ')
        print(mat)
        # since matrix may be very large, string container may not be able to hold it. Therefore we pass it as a JSON object
        stringmat = dumps(mat.tolist())
        stringmat = stringmat.replace(',',' ')
        stringmat = stringmat.replace('.0',',')
        stringmat = stringmat.replace(',]',']')
        stop = time.process_time()
    diff = 1000*(stop-start)
    start = str(start)
    stop = str(stop)
    diff = str(diff)
    return render(request, 'matrix.html', {'Matrix': stringmat, 'Start': start, 'Stop': stop, 'Time': diff})


def transpose(request):
    global mat
    print('Matrix: ')
    print(mat)
    print('\n\n')
    print('Transpose Matrix: ')
    print(mat.T)
    stringmat = dumps(mat.tolist())
    stringmat = stringmat.replace(',',' ')
    stringmat = stringmat.replace('.0',',')
    stringmat = stringmat.replace(',]',']')
    tstringmat = dumps((mat.T).tolist())
    tstringmat = tstringmat.replace(',',' ')
    tstringmat = tstringmat.replace('.0',',')
    tstringmat = tstringmat.replace(',]',']')
    return render(request, 'transpose.html', {'Matrix': stringmat, 'Transpose': tstringmat, 'Start': start, 'Stop': stop, 'Time': diff})