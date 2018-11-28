from abc import ABCMeta,abstractclassmethod
from BoolQuery.ExpParser.Tokens import Tokens
from BoolQuery.ExpParser.TokenParser import TokenParser
from DataStruct.Node import TreeNode

class ExpressionException(Exception):
    pass

class Expressions:
    """ Generate an abstract grammar tree """
    def __init__(self):
        self._parser=TokenParser()
        self._clear()
        pass

    def _next(self):
         token=self._parser.tokenList[self._index]
         self._index+=1
         if isinstance(token,tuple):
             self._curToken=token[0]
             self._curData=token[1]
         else:
             self._curToken=token

    def _clear(self):
        self._curToken=Tokens.End
        self._curData=None
        self._stackWord=[]
        self._stackExp=[Tokens.End]
        self._root=None
        self._index=0
        self._lastToken=Tokens.End

    def getRoot(self):
        return self._root

    def parse(self,str1):
        self._clear()
        self._parser.parse(str1)
        self._curToken=Tokens.Unknown
        while self._curToken != Tokens.End:
            self._next()
            if self._curToken==Tokens.Word:
                self._stackWord.append(TreeNode(self._curData,child=None))
            elif Tokens.isExp(self._curToken):
                #Get piority to decide whether to begin compute
                topp=Tokens.getPiorityInStack(self._stackExp[-1])
                curp=Tokens.getPiority(self._curToken)
                if topp<=curp:
                    self._stackExp.append(self._curToken)
                else:
                    curRoot=None
                    #len(self._stackWord)>0 and len(self._stackExp)>0 and 
                    while (Tokens.getPiority(self._stackExp[-1])>curp):
                        #pop all elements
                        op,count=self._popSameExp()
                        if op==Tokens.ExpLC:#jump
                            break;
                        elif op==Tokens.ExpNot:
                            if count%2==0:
                                continue;#no need for computing such expressions
                            else:
                                words=self._popWords(1)#NOT once
                        else:
                            #once we pop n operators, we need to pop n+1 words, (AND, OR)
                            #if there is already a computed node, pop n words
                            extra=0
                            if curRoot is None:
                                extra=1
                            words=self._popWords(count+extra)
                        #add to tree
                        node = TreeNode(data=op,child=[])
                        for word in words:
                            node.addChild(word)
                        curRoot = self._addToTree(node,curRoot)
                        pass        #while
                    if self._curToken!=Tokens.ExpRC:
                        self._stackExp.append(self._curToken)
                    if curRoot is not None:
                        self._stackWord.append(curRoot)
                        self._root = curRoot
                    if self._curToken==Tokens.End:
                        self._maintainExtraWord()
                    pass            #else
                pass                #elif
            elif Tokens.isInvalid(self._curToken):
                raise ExpressionException("Unexpected "+str(self._curToken))
            pass                    #while
        if(self._root is None):
            self._root=TreeNode(self._stackWord[0].data,child=None)
        else:
            if len(self._stackExp)!=2 or len(self._stackWord)!=1:
                raise ExpressionException("Expression Error")
        print("----expression tree-----")
        print(str(self._root))

    def _maintainExtraWord(self):
        remains=len(self._stackWord)
        if remains<=1:
            return
        self._stackExp.pop()        #pop end
        for i in range(remains-1):
            self._stackExp.append((Tokens.ExpAnd))
        self._parser.tokenList.append((Tokens.End))
        self._curToken=Tokens.ExpAnd


    def _popSameExp(self):
        op = self._stackExp[-1]
        count = 0
        if op==Tokens.ExpLC:
            if self._curToken==Tokens.ExpRC:
                self._stackExp.pop()
                return op,1
            else: 
                return op,0
        while self._stackExp[-1]==op and len(self._stackExp)>0:
            count+=1
            self._stackExp.pop()
        return op,count

    def _popWords(self,count):
        words=[]
        for i in range(count):
            words.append(self._stackWord.pop())
        return words

    #input node that need to be add to root, output the root node
    def _addToTree(self,node,curNode):
        #incomplete expression 
        if Tokens.isTwoComp(node.data) or Tokens.isOneComp(node.data):
            if curNode is None:
                return node
            else:
                node.addChild(curNode)
                curNode=node
                return node
        # other operators
        return curNode





