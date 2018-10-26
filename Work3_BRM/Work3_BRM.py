import sys
import json
import os
import nltk
from textblob import TextBlob
from textblob import Word
import pickle
import random
import DataStruct
import BoolQuery as bq

#==========================
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
#========================
def readTweets():
    f = open("tweets.json")
    lines = f.readlines()
    texts = []
    for line in lines:
        tempObj = json.loads(line)
        texts.append(tempObj['text'])
    return texts;
#=========================
def getData():
    # read files
    texts=readTweets()
    result = load("textContent",1)
    result2 = load("wordDict",1)
    if(result is not None and result2 is not None):
        print("use cache")
        return result2,result,texts;#wordDict,textContent,texts
    print("Get words... Doc ="+str(len(texts)))
    textContent=[]
    wordSet = set([])
    for text in texts:
        words=TextBlob(text).words
        realWord=[]
        for word in words:
            if word.isalpha():
                realWord.append(word.lower())
        textContent.append(realWord)
        for word in realWord:
            wordSet.add(word)

    print("Build dictionary...")
    wordDict={}
    index=-1
    for word in wordSet:
        index+=1
        wordDict[word]=index
    print("Dictionary len="+str(len(wordDict)))
    print("saving...")
    save("wordDict",wordDict,1)
    save("textContent",textContent,1)
    return wordDict,textContent,texts;
#===============
def makeList(wordDict,texts):
    result = load("invertIndexList")
    if result is not None:
        print("use cache")
        return result
    iil=bq.InvertIndexList.InvertIndexList(wordDict,texts)
    print("saving...")
    save("invertIndexList",iil)
    return iil
#====================
def printDocs(list,texts):
    if list is None or len(list)==0:
        print("Found nothing")
        return
    for l in list:
        print(texts[l])

def main():
    wordDict,textWordList,texts=getData()
    print("Processing...")
    iil=makeList(wordDict,textWordList)
    while True:
        print("===============")
        print("Input command:")
        command=input()
        r = bq.ExecuteTree.ExecuteTree.ExecuteQuery(command,iil)
        print("=====result=====")
        print(r)
        printDocs(r,texts)
    return;
    

if __name__=="__main__":
    main();
    #abt=bq.ExpParser.Expressions.Expressions()
    #abt.parse("a&(b|c)&d|!(e&(f|l&m&n)|!(!o&p));")#a&(b|c)&d|!(e&(f|l&m&n)|!(!o&p))    !(!(a))