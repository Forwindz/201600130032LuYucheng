from DataStruct.LinkedList import LinkedList
import math
import json

class InvertIndexList(object):
    """
    wordDict    : a list of word, wordDict[word]=index
    table       : a list of linked lists correspond to each word, each list contains (document index, times)
    docScore    : scored using BM25 method
    docLength   : the length of each document
    """
    def __init__(self, wordDict=None, docWordList=None):
        self.table=[]
        self._currentWordID = 0
        self._currentDocID = 0
        self._totalWord=0
        self._averageDocLength=0
        self._docLength=[]
        if wordDict is None or docWordList is None:
            return
        self.wordDict=wordDict
        self._currentWordID = len(wordDict)
        for word in wordDict:
            self.table.append(LinkedList())
        for doc in docWordList:
            self.appendDoc(doc)
            if self._currentDocID%200==0:
                print("Processing...\t"+str(self._currentDocID)+"/"+str(len(docWordList)),end="\r")
       
    def appendDoc(self,wordList):
        self._docLength.append(len(wordList))
        self._totalWord+=len(wordList)
        for word in wordList:
            index=self.wordDict.get(word,-1)
            if index==-1:
                self._expandWordList(word)
            self.table[index].addIfExistBySeq(self._currentDocID)
        self._currentDocID+=1

    def _expandWordList(self,newWord):
        self.wordDict[newWord]=self._currentWordID
        self.table.append(LinkedList())
        self._currentWordID+=1

    # return each word list cost 
    def generateCostList(self):
        cost=[]
        for l in self.table:
            cost.append(float(len(l))/self._currentDocID)
        return cost

    def getLinkedList(self,word):
        index=self.wordDict.get(word,-1)
        if index<0:
            return LinkedList()
        return self.table[index]

    def computeCost(self,list):
        return float(len(list))/self._currentDocID

    def fullList(self):
        return LinkedList.generateNumList(0,self._currentDocID)

    def __str__(self):
        return self.saveTableToStr()

    def loadTableFromStr(self,lines,wordDict):
        self._currentWordID=len(wordDict)
        self.wordDict=wordDict
        attr=lines[0].split(",")
        self._totalWord=int(attr[0])
        self._currentDocID=int(attr[1].strip("\n"))
        self._docLength=json.loads(lines[1].strip("\n "))
        self.table=[]
        first=0
        for line in lines:
            if first<2:#skip 2 lines
                first+=1
                continue
            line2=line.strip('[]\n')
            idList=line2.split(",")
            ll = LinkedList()
            for idstr in idList:
                idstrs=idstr.strip(' ').split(' ')
                ll.appendTail(int(idstrs[0]),int(idstrs[1]))
            self.table.append(ll)
            pass
        #print(self)

    def saveTableToStr(self):
        s=str(self._totalWord)+","+str(self._currentDocID)+"\n"+str(self._docLength)+"\n"
        for item in self.table:
            s+=str(item)+'\n'
        return s


    #return list: (score,docId)
    def getScore(self,docList,wordList):
        self._averageDocLength=self._totalWord/float(self._currentDocID)
        score=[]
        for doc in docList:
            sc=self._getSingleScore(doc,wordList)
            score.append((sc,doc))
        return sorted(score)

    #for each query word and satisfied documentory
    def _getSingleScore(self,docId,wordList,b=0.2,k=5):
        v=0
        for word in wordList:
            weight=self.table[self.wordDict[word]].find(docId)
            v+=math.log(1+math.log(1+weight))/(1-b+b*self._docLength[docId]/self._averageDocLength)*math.log((self._currentDocID+1)/len(self.table[self.wordDict[word]]))
        return v






