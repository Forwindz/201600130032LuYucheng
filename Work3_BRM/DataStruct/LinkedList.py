from DataStruct.Node import Node
class LinkedList(object):
    """
    First Node is empty
    Default Sequence : low--->high
    """

    def __init__(self):
        self.head=Node(None)
        self.tail=self.head
        self.length=0
        self.iter=None

    def __len__(self):
        return self.length

    def __iter__(self):
        self.iter=self.head
        return self

    def __next__(self):
        self.iter=self.iter.next
        if self.iter is None:
            raise StopIteration
        else:
            return self.iter.data

    def appendTail(self,data):
        node = Node(data)
        self.tail.next = node
        self.tail = node
        self.length+=1

    def _insertMedium(self,preNode,insertNode):
        insertNode.next=preNode.next
        preNode.next=insertNode
        self.length+=1

    def appendBySequence(self,data):
        if self.length<=0:
            self.appendTail(data)
            return
        i = self.head
        while i.next is not None and i.next.data<data:
            i=i.next
        if i.next is None:
            self.appendTail(data)
        else:
            self._insertMedium(i,Node(data))

    def __add__(self,other):
        self.appendTail(other)

    def __str__(self):
        s='[ '
        for item in self:
            s+=str(item)+','
        return s+' ]'

    def __lt__(self, value):
        return len(self)<len(value)
    
    def __le__(self, value):
        return len(self)<=len(value)
    def __gt__(self, value):
        return len(self)>len(value)
    def __ge__(self, value):
        return len(self)>=len(value)
    #return a or b
    @staticmethod
    def unionBySeq(a,b):
        r=LinkedList()
        ai=a.head.next
        bi=b.head.next
        while ai is not None or bi is not None:
            if ai is None:
                r.appendTail(bi.data)
                bi=bi.next
            elif bi is None:
                r.appendTail(ai.data)
                ai=ai.next
            elif ai>bi:
                r.appendTail(bi.data)
                bi=bi.next
            elif ai<bi:
                r.appendTail(ai.data)
                ai=ai.next
            else:#ai==bi
                ai=ai.next
        return r


    #return a and b
    @staticmethod
    def intersectBySeq(a,b):
        r=LinkedList()
        ai=a.head.next
        bi=b.head.next
        while ai is not None and bi is not None:
            if ai>bi:
                bi=bi.next
            elif ai<bi:
                ai=ai.next
            else:#ai==bi
                r.appendTail(ai.data)
                ai=ai.next
        return r

    #return a and not b
    @staticmethod
    def intersectNotBySeq(a,notb):
        r=LinkedList()
        ai=a.head.next
        bi=notb.head.next
        while ai is not None and bi is not None:
            if ai>bi:
                bi=bi.next
            elif ai<bi:
                r.appendTail(ai.data)
                ai=ai.next
            else:#ai==bi
                ai=ai.next
        if bi is None:
            while ai is not None:
                r.appendTail(ai.data)
                ai=ai.next
        return r

    #return full-a
    #equals (full and not a)
    @staticmethod
    def notBySeq(a,full):
        return LinkedList.intersectNotBySeq(full,a)

    @staticmethod
    def generateNumList(f,t):
        r=LinkedList()
        for i in range(f,t):
            r.appendTail(i)
        return r






