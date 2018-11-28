class Node(object):
    """
    data : data
    next : next node
    """
    def __init__(self, data, next=None):
        self.data = data
        self.weight = 1
        self.next = next

    def __str__(self):
        return str(data)

    def __cmp__(stc,dst):
        return self.data==dst.data

    def __gt__(self,other):
        return self.data>other.data

    def __lt__(self,other):
        return self.data<other.data

    def __ge__(self,other):
        return self.data>=other.data

    def __le__(self,other):
        return self.data<=other.data

    def __eq__(self,other):
        return self.data==other.data

class TreeNode:
    """
    data : data
    parent : parent
    """
    def __init__(self, data, parent=None,child=[]):
        self.data = data
        self.parent = parent
        self.child = child

    def addChild(self,node):
        node.changeParent(self)
        self.child.append(node)

    def removeChild(self,node):
        node.changeParent(None)
        self.child.remove(node)

    def changeParent(self,node):
        self.parent=node

    def __str__(self):
        st=2*self.getDepth()*' '+'||'+str(self.data)
        if self.child is not None:
            st+=str(len(self.child))
            for c in self.child:
                st+="\n"+str(c)
        return st;

    def getDepth(self):
        depth=0
        node=self
        while node is not None:
            node=node.parent
            depth+=1
        return depth

