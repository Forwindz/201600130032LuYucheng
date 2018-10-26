from BoolQuery.ExpParser.Tokens import Tokens
class TokenParser(object):
    """
    tokens are stored in tokenList
    each char may generate 0~2 tokens
    """
    def __init__(self):
        self._curChar=''
        self._curToken=Tokens.End
        self._lastIsWord=False
        self.tokenList=[]

    def _appendWord(self):
        if self._lastIsWord:
            self.tokenList.append((Tokens.ExpAnd))
        self.tokenList.append((self._curToken,self._curChar.lower()))
        self._curToken=Tokens.End
        self._curChar=''
        self._lastIsWord=True

    def inputChar(self,char):
        # porcess
        if char in [' ','\t','\n']:
            if self._curToken in [Tokens.Word,Tokens.Num]:
                self._appendWord()
            return
        elif char.isalpha():#a~z
            self._curChar+=char
            if self._curToken!=Tokens.Num:
                self._curToken=Tokens.Word
            return 
        elif char.isdigit():#0~9
            self._curChar+=char
            if self._curToken!=Tokens.Word:
                self._curToken=Tokens.Num
            return
        elif self._curToken!=Tokens.End:#other input
            #end of word or number
            self._appendWord()
            pass

        if char=='&':
            self.tokenList.append((Tokens.ExpAnd))
        elif char=='|':
            self.tokenList.append((Tokens.ExpOr))
        elif char=='!':
            self.tokenList.append((Tokens.ExpNot))
        elif char=='(':
            self.tokenList.append((Tokens.ExpLC))
        elif char==')':
            self.tokenList.append((Tokens.ExpRC))
        elif char==';':
            self.tokenList.append((Tokens.End))
        else:
            self.tokenList.append((Tokens.Unknown))
        if self.tokenList[-1]!=Tokens.Word:
            self._lastIsWord=False

    def parse(self,str):
        for char in str:
            self.inputChar(char)


