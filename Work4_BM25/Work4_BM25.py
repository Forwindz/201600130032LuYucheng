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
from nltk.corpus import stopwords

#==========================
def save(name,data,mode=0):
    if(mode==1 and type(data) in [list,dict,set]):
        with open(name+".json",'w') as f:
            json.dump(data,f)
    elif mode==0:
        with open(name+".npy",'wb') as f:
            pickle.dump(data,f,True)
    elif mode==2:
        with open(name+".txt",'w') as f:
            f.write(str(data))
    return;
#=========================
def load(name,mode=0):
    if(mode==1):
        if not os.path.exists(name+".json"):
            return None
        with open(name+".json",'r') as f:
            data = json.load(f)
    elif mode==0:
        if not os.path.exists(name+".npy"):
            return None
        with open(name+".npy",'rb') as f:
            data = pickle.load(f)
    elif mode==2:
        if not os.path.exists(name+".txt"):
            return None
        with open(name+".txt",'r') as f:
            return f.readlines()
    return data;
#========================
def readTweets():
    f = open("tweets.json")
    lines = f.readlines()
    texts = []
    ids=[]
    for line in lines:
        tempObj = json.loads(line)
        texts.append(tempObj['text'])
        ids.append(tempObj['tweetId'])
    return texts,ids;
#=========================
def getData():
    # read files
    texts,ids=readTweets()
    result = load("textContent",1)
    result2 = load("wordDict",1)
    if(result is not None and result2 is not None):
        print("use cache")
        return result2,result,texts,ids;#wordDict,textContent,texts
    print("Get words... Doc ="+str(len(texts)))
    textContent=[]
    wordSet = set([])
    for text in texts:
        words=TextBlob(text.replace('-',' ')).words
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
    return wordDict,textContent,texts,ids;
#===============
def makeList(wordDict,texts):
    result = load("invertIndexList",2)
    if result is not None:
        print("use cache")
        ll=bq.InvertIndexList.InvertIndexList()
        ll.loadTableFromStr(result,wordDict)
        return ll
    iil=bq.InvertIndexList.InvertIndexList(wordDict,texts)
    print("saving...")
    save("invertIndexList",iil,2)
    return iil
#====================
def printDocs(list,texts):
    if list is None or len(list)==0:
        print("Found nothing")
        return
    print("Total:\t[ "+str(len(list))+"]")
    if len(list)>40:
        print("print all tweets? Y/n")
        con=input()
        if con[0]!='Y':
            return
    #print(list)
    for l in reversed(list):
        print(str(l[0])+" score\t"+str(texts[l[1]]))
#===================
def readQuery(filePath):
    lines=load(filePath,2)
    query=[]
    qid=[]
    for line in lines:
        if len(line)>10 and line[0]=='<' and line[6]=='>':
            query.append(line.replace("<query>","").replace("</query>","").strip("\n "))
        elif len(line)>10 and line[0]=='<' and line[1]=='n':
            qid.append(int(line.replace("<num> Number: MB","").replace(" </num>","").strip("\n ")))
    return query,qid
#=================
def preprocessInput(s):
    result=''
    for ch in s.lower():
        if ch>='a' and ch<='z' or ch==' ':
            result+=ch
    words=TextBlob(result).words
    sp=set(stopwords.words('english'))
    result=''
    for word in words:
        if word not in sp:
            result+=word+" "
            
    return result.strip();
#=================
def main():
    wordDict,textWordList,texts,textids=getData()
    print("Processing...")
    iil=makeList(wordDict,textWordList)
    while True:
        print("===============")
        print("Input command:")
        command=input()
        r = bq.ExecuteTree.ExecuteTree.ExecuteQuery(command,iil)
        print("=====result=====")
        printDocs(r,texts)
    return;

def queryTest():
    wordDict,textWordList,texts,textids=getData()
    print("Processing...")
    iil=makeList(wordDict,textWordList)
    q,qid = readQuery("query")
    s=""    #result string
    for i,qstr in enumerate(q):
        qp = preprocessInput(qstr)
        ans = bq.ExecuteTree.ExecuteTree.ExecuteQuery(qp,iil)
        print(">"+str(qid[i])+"Search ["+qp+"], Result : "+str(len(ans)))
        for doc in ans:
            s+=str(qid[i])+" "+str(textids[doc[1]])+"\n"
    print("saving results..")
    save("query_result",s,2)

if __name__=="__main__":
    #main()
    queryTest()