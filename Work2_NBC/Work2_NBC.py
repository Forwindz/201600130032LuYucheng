#!/usr/bin/python 
# -*- coding: utf-8 -*-

import os
import nltk
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from textblob import Word
import numpy as np
import collections as cl
import math
import json
import pickle
import random
#==========================
#https://www.jianshu.com/p/b129225c661d
def save(name,data,mode=0):
    if(mode==1 and type(data) in [list,dict,set]):
        with open(name+".json",'w') as f:
            json.dump(data,f)
    else:
        with open(name+".npy",'wb') as f:
            pickle.dump(data,f,True)
    return;
#=========================
def load(name,mode=0):
    if(mode==1):
        if not os.path.exists(name+".json"):
            return None
        with open(name+".json",'r') as f:
            data = json.load(f)
    else:
        if not os.path.exists(name+".npy"):
            return None
        with open(name+".npy",'rb') as f:
            data = pickle.load(f)
    return data;
#=========================
def calcByesMatrix(nowList,wordDict,types,typeMatrix):

    #countT = load("ByesMatrix")
    #if countT is not None:
    #    return countT;
    count = np.zeros((len(types),len(nowList)))
    wordKindCount = len(nowList)
    typeHasWord={} # how many words each type has 
    for typeIndex in range(len(types)):
        typeHasWord[typeIndex] = sum(typeMatrix[typeIndex])

    for word,wordIndex in nowList.items():
        #previously smooth and log
        for typeIndex in types.values():
            count[typeIndex][wordIndex]=math.log((typeMatrix[typeIndex][wordIndex]+1)/(typeHasWord[typeIndex]+wordKindCount))
    save("ByesMatrix",count)
    return count;
#=========================
def classification(byesMatrix,types,article,nowList):
    result=[];# typeIndex:value
    for i in range(len(types)):
        result.append(0)

    for word in article:
        if word not in nowList.keys():
            continue;
        wordIndex = nowList[word]
        for typeIndex in range(len(types)):
            result[typeIndex]+=byesMatrix[typeIndex][wordIndex]
    #find max
    maxV=result[0]
    maxType=0
    for i in range(len(types)):
        if result[i]>maxV:
            maxV=result[i]
            maxType=i

    return maxType;
#==========================
def getRealType(fileName,types):
    names = fileName.split("/")
    return types[names[1]];
#==================================
def getTypes(files):
    types={}
    typeIndex=0
    for fileName in files:
        filesPart = fileName.split("/")
        fileType = filesPart[1]
        if fileType not in types.keys():
            types[fileType]=typeIndex
            typeIndex+=1
    return types;
#==================================
def getTypesInfo(files,wordList,nowList):
    types=getTypes(files)
    #words' frequency of each type
    count = np.zeros((len(types),len(nowList)),dtype=int)
    for id,fileN in enumerate(files):
        filesPart = fileN.split("/")
        ft = types[filesPart[1]]
        for word in wordList[fileN]:
            count[ft][nowList[word]]+=1
    print("Saving...")
    save("TypeMatrix",count)
    save("TypeNames",types,1)
    return count,types;
#======================================================
def sperateDate(files):
    types=getTypes(files);
    trainFiles=[]
    testFiles=[]
    for fileName in files:
        ft = getRealType(fileName,types)
        if random.randint(0,100)<=90:
            trainFiles.append(fileName)
        else:
            testFiles.append(fileName)
    print("Train="+str(len(trainFiles))+" Test="+str(len(testFiles)))
    save("TrainFiles",trainFiles,1)
    save("TestFiles",testFiles,1)
    return trainFiles,testFiles;
#======================================================
def trainAndTest(files,nowList,wordList,wordDict):
    print("sperate files...")
    trainFiles,testFiles = sperateDate(files)

    print("compute basic Matrix...")
    typeMatrix,types = getTypesInfo(trainFiles,wordList,nowList)

    print("compute byes Matrix...")
    byesMatrix = calcByesMatrix(nowList,wordDict,types,typeMatrix)

    print("begin to test model...")
    totalDoc = len(testFiles)
    right=0
    wrong=0

    for i in range(totalDoc):
        article = wordList[testFiles[i]]
        fileName = testFiles[i]
        result1=classification(byesMatrix,types,article,nowList)
        result2=getRealType(fileName,types)
        if result1==result2:
            right+=1
        else:
            wrong+=1
        if i%100==0:
            print("Testing... "+str(i)+"/"+str(totalDoc)+" √ "+str(right)+" || ×"+str(wrong)+" \tcur:"+str(result1)+"-"+str(result2))
    
    print("Result "+str(totalDoc)+" √ "+str(right)+" || ×"+str(wrong))
    acc=float(right)/totalDoc*100
    print("Acc "+str(acc)+" %")
    return acc;
def main():
    files=load("files",1)
    nowList=load("nowList",1)
    wordList=load("wordList",1)
    wordDict = load("wordDict",1)
    print("load complete")
    print("total word = "+str(len(wordList)))

    trainAndTest(files,nowList,wordList,wordDict);

    return;
    

if __name__=="__main__":
    main();