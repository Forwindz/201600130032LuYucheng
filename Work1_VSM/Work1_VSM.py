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
        if not ((char>='a' and char<='z')or(char>='0' and char<='9') or char in enableSymbol):
            return False;
    return True;
#==========================
#https://www.jianshu.com/p/b129225c661d
def save(name,data):
    #folder = os.path.exists(path)
    with open(name+".json",'w') as f:
        if type(data) in [set,list,dict]:
            json.dump(data,f)
        else:
            f.write(str(data))
    return;
#=========================
#nltk.download('punkt')
#nltk.download('stopwrods')
#nltk.download('wordnet')
files=[]
getAllFiles('20news-18828',files)
#print(s) #打印结果
nowList = {}
nowCount=np.zeros((1,1),dtype=int)
sws = stopwords.words('english')
st = PorterStemmer()
files_count=len(files);
document=-1
wordList=[]
wordDict={}
#files=[files[41],files[151],files[120]]
enableSymbol = set(['-','\''])
print("Begin!")
for file_input in files:
    document+=1
    if document%10==0:
        print("Reading document "+str(document)+"/"+str(files_count)+" \t"+file_input)
    f = open(file_input, mode='r', encoding='utf-8',errors='ignore')
    article=f.read()
    f.close()
    wordList.append([])
    for word in TextBlob(article).words:
        new_word=word.lower()
        if not checkWord(new_word,enableSymbol):
            continue
        new_word = Word(st.stem(new_word)).lemmatize()
        if new_word in sws:
            continue
        else:
            wordList[document].append(new_word)
            wordDict[new_word]=1+wordDict.get(new_word,0)

print("complete reading")
index=0

for word,times in wordDict.items():
    #if times>2:
        nowList[word]=index
        index+=1

wordExistInDoc = np.zeros((1,len(nowList)))
for document in wordList:
    for word,index in nowList.items():
        if word in document:
            wordExistInDoc[0][index] +=1
    pass

print("saving...")
save("nowList",nowList)
save("wordDict",wordDict)
save("wordList",wordList)
save("wordExistInDoc",wordExistInDoc)
print("size= "+str(len(files))+","+str(len(nowList)))
#nowCount = np.zeros((len(files),len(nowList)),dtype=int)
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
    tf_idf=[]
    for i in range(len(nowList)):
        tf_idf.append(float(nowCount[0][i])/articleLen*math.log10(files_count/wordExistInDoc[0][i]))
    save("mats/"+files[document].replace('/','_'),tf_idf)

print("Done")