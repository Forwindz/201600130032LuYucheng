from DataStruct.LinkedList import LinkedList
class InvertIndexList(object):
    """
    wordDict    : a list of word, wordDict[word]=index
    table       : a list of linked list correspond to each word, each list contains some document indexes
    """
    def __init__(self, wordDict, docWordList):
        self.wordDict=wordDict
        self.table=[]
        self._currentWordID = len(wordDict)
        self._currentDocID = 0
        for word in wordDict:
            self.table.append(LinkedList())
        for doc in docWordList:
            self.appendDoc(doc)
            if self._currentDocID%200==0:
                print("Processing...\t"+str(self._currentDocID)+"/"+str(len(docWordList)))
       
    def appendDoc(self,wordList):
        for word in wordList:
            index=self.wordDict.get(word,-1)
            if index==-1:
                self._expandWordList(word)
            self.table[index].appendBySequence(self._currentDocID)
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
        s='[ '
        for item in self.table:
            s+=str(item)+','
        s+=' ]'
        return s
     

