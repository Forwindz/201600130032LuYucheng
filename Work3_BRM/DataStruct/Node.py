class Node(object):
    """
    data : data
    next : next node
    """
    def __init__(self, data, next=None):
        self.data = data
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

    def __str_inner(self,prefix):
        st=''
        s1=None
        s1=prefix+'| '
        if self.lc is not None:
            st+=prefix+'乚'+str(self.lc.data)
            st+="\n"+self.lc.__str_inner(s1)
        s1=prefix+'  '
        if self.rc is not None:
            st+=prefix+'乚'+str(self.rc.data)
            st+="\n"+self.rc.__str_inner(s1)
        return st

    def __str__(self):
        return str(self.data)+"\n"+self.__str_inner('');

    def getDepth(self):
        depth=0
        node=self
        while node is not None:
            node=node.parent
            depth+=1
        return depth

