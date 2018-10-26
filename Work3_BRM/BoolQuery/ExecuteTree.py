from BoolQuery.ExpParser import *
from BoolQuery.ExpParser.Tokens import *
from BoolQuery.InvertIndexList import *
import heapq
class ExecuteTree(object):
    """description of class"""

    def __init__(self,treeRoot,list):
        self._root=treeRoot
        self._list=list
        self._cost=list.generateCostList()
        self._full=list.fullList()

    def compute(self):
        return self._computeNode(self._root)

    @staticmethod
    def ExecuteQuery(command,list):
        if command[-1]!=';':
            command+=';'
        abt=BoolQuery.ExpParser.Expressions.Expressions()
        try:
            abt.parse(command)
            exe = BoolQuery.ExecuteTree.ExecuteTree(abt.getRoot(),list)
            return exe.compute()
        except:
            print("There might be some errors in your command.")
            return None
        

    #compute Node and return a linked list
    def _computeNode(self,node):
        if node.child is None:
            return self._list.getLinkedList(node.data)
        #op node
        if node.data==Tokens.ExpAnd:
            return self._and(node)
        elif node.data==Tokens.ExpOr:
            return self._or(node)
        elif node.data==Tokens.ExpNot:
            return self._not(node)
        return None

    def _and(self,node):
        v = self._evaluate(node)
        minCost = heapq.nsmallest(1,v)[0]
        if minCost[0]==0:
            return LinkedList()
        while(len(v)>1):
            l1= heapq.heappop(v)
            l2= heapq.heappop(v)
            lr=LinkedList.intersectBySeq(l1[1],l2[1])
            heapq.heappush(v, (self._list.computeCost(lr),lr) )
        return heapq.heappop(v)[1]

    def _or(self,node):
        v = self._evaluate(node)
        while(len(v)>1):
            l1= heapq.heappop(v)
            l2= heapq.heappop(v)
            lr=LinkedList.unionBySeq(l1[1],l2[1])
            heapq.heappush(v, (self._list.computeCost(lr),lr) )
        return heapq.heappop(v)[1]

    def _not(self,node):
        v = self._evaluate(node)
        return LinkedList.notBySeq(heapq.heappop(v)[1], self._full)

    # evaluate compute cost for each list, return heap [(cost,linkedlist),(),()...]
    def _evaluate(self,node):
        v=[]#heapq.heapify()
        for c in node.child:
            if isinstance(c.data,str):
                heapq.heappush(v,(self._getCost(c.data),self._list.getLinkedList(c.data)))
            else:
                llr = self._computeNode(c)
                heapq.heappush(v,(self._list.computeCost(llr),llr))
        return v

    def _getCost(self,word):
        index=self._list.wordDict.get(word,-1)
        if index<0:
            return 0
        return self._cost[index]





