from DataStruct.LinkedList import LinkedList
class InvertIndexList(object):
    """
    wordDict    : a list of word, wordDict[word]=index
    table       : a list of linked list correspond to each word, each list contains some document indexes
    """
    def __init__(self, wordDict=None, docWordList=None):
        self.table=[]
        self._currentWordID = 0
        self._currentDocID = 0
        if wordDict is None or docWordList is None:
            return
        self.wordDict=wordDict
        self._currentWordID = len(wordDict)
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
        return self.saveTableToStr()

    def loadTableFromStr(self,lines,wordDict):
        self._currentWordID=len(wordDict)
        self.wordDict=wordDict
        self._currentDocID=int(lines[0].split(",")[1].strip("\n"))
        self.table=[]
        first=True
        for line in lines:
            if first:
                first=False
                continue
            line2=line.strip('[]\n')
            idList=line2.split(",")
            ll = LinkedList()
            for id in idList:
                ll.appendTail(int(id))
            self.table.append(ll)
            pass
        #print(self)

    def saveTableToStr(self):
        s=str(self._currentWordID)+","+str(self._currentDocID)+"\n"
        for item in self.table:
            s+=str(item)+'\n'
        return s

