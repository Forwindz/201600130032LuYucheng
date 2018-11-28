from enum import Enum, unique

@unique
class Tokens(Enum):
    """Tokens"""
    Unknown =   -2
    End     =   -1
    Num     =   0
    Word    =   1
    ExpAnd  =   2
    ExpOr   =   3
    ExpNot  =   4
    ExpLC   =   5
    ExpRC   =   6

    dicts={
    ExpAnd  :   2,
    ExpOr   :   1,
    ExpNot  :   3,
    ExpLC   :   100,
    ExpRC   :   0,
    End     :   -1
    }
    @staticmethod
    def getPiority(token):
        if      token==Tokens.ExpAnd:  return 2
        elif    token==Tokens.ExpOr:   return 1
        elif    token==Tokens.ExpNot:  return 3
        elif    token==Tokens.ExpLC:   return 100
        elif    token==Tokens.ExpRC:   return -1
        elif    token==Tokens.End:     return -2
        return -100

    @staticmethod
    def getPiorityInStack(token):
        if      token==Tokens.ExpAnd:  return 2
        elif    token==Tokens.ExpOr:   return 1
        elif    token==Tokens.ExpNot:  return 3
        elif    token==Tokens.ExpLC:   return 0
        elif    token==Tokens.ExpRC:   return 101
        elif    token==Tokens.End:     return -2
        return -100
    @staticmethod
    def isExp(token):
        return token in [Tokens.ExpAnd,Tokens.ExpOr,
                         Tokens.ExpNot,Tokens.ExpLC,
                         Tokens.ExpRC,Tokens.End]

    @staticmethod
    def isInvalid(token):
        return token==Tokens.Num or token==Tokens.Unknown
    
    @staticmethod
    def isTwoComp(token):
        return token==Tokens.ExpAnd or token==Tokens.ExpOr
    
    @staticmethod
    def isOneComp(token):
        return token==Tokens.ExpNot
        


