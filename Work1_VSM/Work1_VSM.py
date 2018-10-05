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
#参考：https://juejin.im/entry/5aa34b10f265da2381553b87
#==========================

def getAllFiles(path, files):
    f= os.listdir(path) #得到文件夹下的所有文件名称
    for file in f: #遍历文件夹
        file=path+'/'+file
        if (os.path.isdir(file)): #判断是否是文件夹，不是文件夹才打开
            getAllFiles(file,files)
        else:
            files.append(file)
    return;
#==========================
#   row : document
#   column : word
def addList(nowList,nowCount,nowDoc,addWord):
    if nowCount[0][0]==0:
        nowList.append(addWord)
        nowCount[0][0]+=1
    elif not addWord in nowList:
        nowList.append(addWord)
        tempVec = np.zeros((nowCount.shape[0],1),dtype=int)
        tempVec[nowCount.shape[0]-1][0] = 1
        nowCount=np.concatenate((nowCount,tempVec),axis=1)
    else:
        nowCount[nowDoc][nowList.index(addWord)]+=1
    return nowCount;
#==========================
def extendCount(nowCount):
    if(nowCount[0][0]==0):
        return nowCount;
    tempVec=np.zeros((1,nowCount.shape[1]),dtype=int)
    nowCount = np.concatenate((nowCount,tempVec),axis=0)
    return nowCount;
#==========================
#https://blog.csdn.net/henni_719/article/details/76087491
def checkWord(word,enableSymbol):
    if len(word)<=1:
        return False
    
    for char in word:
        if not ((char>='a' and char<='z') or char in enableSymbol):
            return False;
    return True;
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
def getWords(files):

    wordList = load("wordList",1)
    wordDict = load("wordDict",1)
    nowList = load("nowList",1)
    if(wordList!=None and wordDict!=None and nowList!=None):
        print("Exist cache!")
        return (wordList,wordDict,nowList)


    wordDict={}
    nowList = {}
    sws = stopwords.words('english')
    st = PorterStemmer()
    files_count=len(files);
    wordList={}
    
    enableSymbol = set(['-','\''])

    document=-1
    for file_input in files:
        document+=1
        if document%10==0:
            print("Reading document "+str(document)+"/"+str(files_count)+" \t"+file_input)
        f = open(file_input, mode='r', encoding='utf-8',errors='ignore')
        article=f.read()
        f.close()
        wordList[file_input]=[]
        for word in TextBlob(article).words:
            new_word=word.lower()
            if not checkWord(new_word,enableSymbol):
                continue
            new_word = Word(st.stem(new_word)).lemmatize()
            if new_word in sws:
                continue
            else:
                wordList[file_input].append(new_word)
                wordDict[new_word]=1+wordDict.get(new_word,0)

    print("complete reading")

    index=0
    removeWords=[]
    print("get words...")
    for word,times in wordDict.items():
        if times>2:
            nowList[word]=index
            index+=1
            if index%10000==0 :
                print("word "+str(index))
        else:
            removeWords.append(word)
    print("remove words...")
    listIndex=0;
    for id in wordList.keys():
        listIndex+=1
        if(listIndex % 20==0):
            print("removing..."+str(listIndex))
        temp = filter(lambda x:x not in removeWords,wordList[id])
        wordList[id]=[i for i in temp]
    print("saving...")
    #save as json to save space
    save("nowList",nowList,1)   #use this list
    save("wordDict",wordDict,1) #all word and exists times
    save("wordList",wordList,1) #all word for each document
    save("files",files,1)
    return (wordList,wordDict,nowList);
#=============================================
def getTF_IDF(wordList,wordDict,nowList,files):
    print("words exist in document...")
    wordExistInDoc = np.zeros((1,len(nowList)))
    docIndex=-1
    for document in wordList:
        docIndex+=1;
        if docIndex%100==0:
            print("Scanning words at doc \t"+str(docIndex))
        for word,index in nowList.items():
            if word in document:
                wordExistInDoc[0][index] +=1
        pass
    files_count=len(files)
    print("size= "+str(files_count)+","+str(len(nowList)))
    document = -1
    print("begin to compute")

    for articles in wordList:
        document+=1
        nowCount = np.zeros((1,len(nowList)))
        if document%10==0:
            print("Computing document "+str(document)+"/"+str(files_count))
        for word in articles:
            v=nowList.get(word,-1)
            if v==-1:
                continue
            nowCount[0][nowList[word]]+=1
            pass
        articleLen=len(articles)
        tf_idf={}
        simple_count={}
        for i in range(len(nowList)):
            if nowCount[0][i]>0:
                simple_count[i]=nowCount[0][i]
                tf_idf[i]=float(nowCount[0][i])/articleLen*math.log10(files_count/wordExistInDoc[0][i])
        #save as npy to save space
        save("mats/"+files[document].replace('/','_'),tf_idf)           #tf_idf
        save("mats2/"+files[document].replace('/','_'),simple_count)    #count
    return;
#==========================

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)  
    return;
#==========================
def main():
    #nltk.download('punkt')
    #nltk.download('stopwrods')
    #nltk.download('wordnet')
    files=[]
    getAllFiles('20news-18828',files)
    #files=[files[i*100] for i in range(100)]#test only
    print("Begin!")
    wordList,wordDict,nowList = getWords(files)
    mkdir("mats")
    mkdir("mats2")
    getTF_IDF(wordList,wordDict,nowList,files)

    print("Done")
    return;
#============================
if __name__=="__main__":
    main();