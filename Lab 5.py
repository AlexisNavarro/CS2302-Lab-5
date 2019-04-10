# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 15:44:41 2019

@author: Alexis Navarro
CS2302 
MW 1:30-2:50 PM
Professor:Olac Fuentes
Purpose of this code is be able to use binary search trees and hash tables with the use of a text file
with the use of a text file I need to find the similarities among words by using one of the files and using another file that contains the words that 
will be used. 
"""
import numpy as np
import time
import math
import statistics

class BST(object):
    # Constructor
    def __init__(self, item, left=None, right=None):  
        self.item = item
        self.left = left 
        self.right = right      
        
def Insert(T,newItem):
    if T == None:
        T =  BST(newItem)
    elif T.item > newItem:
        T.left = Insert(T.left,newItem)
    else:
        T.right = Insert(T.right,newItem)
    return T





        

    
#------------------------------------------------------------------------------
class HashTableC(object):
    # Builds a hash table of size 'size'
    # Item is a list of (initially empty) lists
    # Constructor
    def __init__(self,size):  
        self.item = []
        for i in range(size):
            self.item.append([])
        
def InsertC(H,k,l):
    # Inserts k in appropriate bucket (list) 
    # Does nothing if k is already in the table
    b = h(k,len(H.item))
    H.item[b].append([k,l]) 
   
def FindC(H,k):
    # Returns bucket (b) and index (i) 
    # If k is not in table, i == -1
    b = h(k,len(H.item))
    for i in range(len(H.item[b])):
        if H.item[b][i][0] == k:
            return b, i, H.item[b][i][1]
    return b, -1, -1
 
def h(s,n):
    r = 0
    for c in s:
        r = (r*255 + ord(c))% n
    return r

def loadFactor(H,i):
    return i/len(H.item)


#------------------------------------------------------------------------------
#BINARY SEARCH TREE
#method to begin creating the binary search Tree
def Building_BST(f1,f2):
    T=None
    
    start_Time=int(time.time())#starting time
    
    for line in f1:
        info = line.split(' ')
        T=Insert(T,[info[0],np.array(info[1:]).astype(np.float)]) #inserts the words and embeddings of the text file
    
    end_Time = int(time.time())#ending time
    
    print('Binary Search Tree Stats:')
    print('Number of Nodes is: ',numNodes(T))
    print('Height: ', getHeight(T))
    print('Running time for Binary Search Tree Construction: ',(end_Time-start_Time))
    print('\n Reading word file to determine similarities')
    
    start_Time2=int(time.time())
    
    for line2 in f2:
        data = line2.split(',')
        e0 = findWord(T,data[0])#returns the list when found
        e1 = findWord(T,data[1])
        print("Similarity", data[0:2], " = ", round(np.sum(e0 * e1) / (math.sqrt(np.sum(e0 * e0)) * math.sqrt(np.sum(e1 * e1))), 4))  # compute the similarity
    end_Time2=int(time.time())
    print('\nRunning time for binary search tree query processing: ',(end_Time2-start_Time2))


def findWord(T,k):
    t = T  
    while t is not None:  
        if t.item[0] == k:
            #temp.item[1]
            return t.item[1]
        elif t.item[0] > k:  
            t= t.left
        elif t.item[0]<k:  
            t = t.right
    return None 

#counts the number of nodes in the tree
def numNodes(T):
    if T is None:
        return 0
    else:
        return 1 + numNodes(T.left)+numNodes(T.right)
    return 0

#get height of the tree
def getHeight(T):
    if T is None:
        return 0
    leftH = getHeight(T.left)
    rightH = getHeight(T.right)
    
    if rightH<leftH:
        return leftH+1
    else:
        return rightH+1
    

#------------------------------------------------------------------------------
#HASH TABLE
#Had to make the hash table differently in order to add the string fields into the table
def Building_Hash(f1,f2):
    H=HashTableC(29)
    print('Hash Table Stats: ')
    print('Initial Table Size: ',len(H.item))
    
    
    count=0
    for line in f1: # this for loop is only used for the text file provided to us
        info = line.index(' ')# gets the index of the first character in the file
        word=line[:info]
        embedding = np.fromstring(line[info:-1],dtype=float,sep=' ')  #makes the embedding
        
        if loadFactor(H,count)==1:  # if statement to check if the load factor is 1
            H=doubleSize(H)
            InsertC(H,word,embedding)
            count+=1
        else:
            InsertC(H,word,embedding)
            count+=1
        
    List=list() #makes an empty list to store our information of the file
    
    startTime=int(time.time())
    
    for line in f2:#This for loop used the word file made by me for this program
        info= line.index(',') # gets the index of the first character in the file
        word=line[:info]#makes/gets the first word
        word2=line[info+1:-1]#gets the second word
        List.append([word,word2])
        
        data=line.split(",")
        e0=find_Hash(H,data[0]) #returns the list when found
        e1=find_Hash(H,data[1])
        print("Similarity", data[0:2], " = ", round(np.sum(e0 * e1) / (math.sqrt(np.sum(e0 * e0)) * math.sqrt(np.sum(e1 * e1))), 4))  # compute the similarity
    endTime=int(time.time())  
        
    print('\nFinal Table Size: ', len(H.item))
    print('Load Factor: ',loadFactor(H,num_items(H)))
    print('Percentage of empty lists: ',round((Empty(H)/len(H.item)),2))
    print('Standard deviations of the lengths of the lists: ',round(statistics.stdev(len_OfList(H))))
    print('\nReading word file to determine similarities')
    
    print('Running time for Hash table query construction: ',(endTime-startTime))
    
    
    
#method to find the number of items in the hash table
def num_items(H):
    Num=0
    for i in range(len(H.item)):
        Num+=len(H.item[i])
    return Num

def Empty(H):
    count=0
    for i in range(len(H.item)):
        if len(H.item[i])==0:
            count+=1
    return count

def find_Hash(H,k):
    b=h(k,len(H.item))
    for i in range(len(H.item[b])):
        if H.item[b][i][0]==k:
            return H.item[b][i][1]
    return -1

#method to be used to find the length of the standard diviation
def len_OfList(H):
    L=[]
    for i in range(len(H.item)):
        L.append(len(H.item[i]))
    return L

#method to double the size of the table
def doubleSize(H):
    newHash=HashTableC(2*len(H.item)+1)
    for i in range(len(H.item)):
        for j in range(len(H.item[i])):
            if H.item[i]==None:
                print()
            else:
                InsertC(newHash,H.item[i][j][0],H.item[i][j][1])
    return newHash
    


#------------------------------------------------------------------------------
#MAIN
    
print('Choose table implementation')  
x=input('Do you want a Binary Search Tree (BST) or Hash Table with Chaining (HT)? select 1 for BST or 2 for HT: ')

f1 = open('glove.6B.50d.txt',encoding='utf-8') #uses the text provided to be read later on
f2 = open('List.txt',encoding='utf-8') #uses my own text file to be read later on

if int(x) == 1:
    print('Building Binary Search Tree')
    print(Building_BST(f1,f2))
elif int(x) == 2 :
    print('Building Hash Table')
    print(Building_Hash(f1,f2))
else:
    print ('input not found')
f1.close()
f2.close()
print()
