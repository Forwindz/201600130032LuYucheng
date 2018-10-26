from BoolQuery.ExpParser.Expressions import *
class Optimizer(object):
    """description of class"""
    def __init__(self,tree):
        self._tree=tree

    def optimize(self):
        if self._tree.child is not None:
            self.checkNot(self._tree)
            self.checkSameLevelOp(self._tree,self._tree.data)
        pass

    #collapse not not EXPRESSION-->EXPRESSION
    def checkNot(self,node):
        appendNode=[]
        if node.child is not None:                              #node
            for c in node.child:
                if c.data==Tokens.ExpNot and c.child is not None:
                    for c2 in c.child:                          #node->not
                        if c2.data==Tokens.ExpNot:              #node->not->not
                            appendNode.append(c2.child)         #node->not->not->child
        for list in appendNode:             
            for ele in list:
                node.child.append(ele)                          #node->child

    #collapse (a and b) and c --> a,b,c and
    def checkSameLevelOp(node,checkToken):
        appendNode=[]
        if node.child is not None:
            for c in node.child:
                if c.child is not None and c.data==checkToken:
                    appendNode+=checkSameLevelOp(c,checkToken)      # op---[word,op,word...]
                elif c.child is None:
                    appendNode.append(c)                            # word
                elif c.data==Tokens.ExpAnd or c.data==Tokens.ExpOr:
                    checkSameLevelOp(c,c.data)                      # other op   
                    appendNode.append(c)
                else:                                               # not
                    checkSameLevelOp(c,checkToken)
                    appendNode.append(c)
        node.child = appendNode
        return appendNode


    def checkRepeatChild(self,node):
        if node.child is None: 
            return
        strs=set([])
        setCount=0
        for c in node.child:                #get all strings
            if isinstance(c.data,str):
                strs.add(c.data)
                setCount+=1
        if setCount>len(strs):              #reconstruct children
            newChild=[]
            for c in node.child:
                if not isinstance(c.data,str):
                    newChild.append(c)
                    c.parent=node
            for word in strs:
                newChild.append(TreeNode(data=word,parent=node,child=None))
        node.child=newChild


                


                    


