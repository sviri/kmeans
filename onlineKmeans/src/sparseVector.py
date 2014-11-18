import sys
from numpy import array, sum, float32, uint32

class SparseVector:
    def __init__(self, d, kvList):
        self.d = d
        kvList = filter(lambda kv: kv[0] >= 0 and kv[0] < self.d, kvList)
        kvList.sort()
        self.nnzs = array([kv[0] for kv in kvList], dtype=uint32)
        self.data = array([kv[1] for kv in kvList], dtype=float32)
        self.shape = (1,self.d)
        self.length = len(self.nnzs)
        
        self._normSquare = sum(self.data**2)
    
    def getNumNnz(self):
        return len(self.nnzs)
    
    def getNormSquare(self):
        return self._normSquare
    
    def dot(self, other):
        iSelf=0 
        iOther=0
        dotProduct = 0.0
        while iSelf < self.length and iOther < other.length:
            nnzSelf = self.nnzs[iSelf]
            nnzOther = other.nnzs[iOther]
            if nnzSelf == nnzOther:
                dotProduct+=self.data[iSelf]*other.data[iOther]
                iSelf+=1
                iOther+=1
            elif nnzSelf < nnzOther:
                iSelf+=1
            elif nnzSelf > nnzOther:
                iOther+=1  
        return dotProduct
    
    def transpose(self):
        return self

    def distSquare(self,other):
        return self._normSquare + other._normSquare - 2*self.dot(other)
        
    def __add__(self, other):
        assert(self.shape == other.shape)
        iSelf=0 
        iOther=0
        kvList = []
        while iSelf < self.length and iOther < other.length:
            nnzSelf = self.nnzs[iSelf]
            nnzOther = other.nnzs[iOther]
            if nnzSelf == nnzOther:
                kvList.append( (nnzSelf, self.data[iSelf]+other.data[iOther]))
                iSelf+=1
                iOther+=1
            elif nnzSelf < nnzOther:
                kvList.append( (nnzSelf, self.data[iSelf]))
                iSelf+=1
            elif nnzSelf > nnzOther:
                kvList.append( (nnzOther, other.data[iOther]))
                iOther+=1  
        return SparseVector(self.shape[1], kvList)
        
        
if __name__ == "__main__":
    d = 30
    sv1 = SparseVector(d, [(1,3.1),(23,0.1),(13,13)])
    sv2 = SparseVector(d, [(12,3.1),(23,0.1),(43,-0.4)])
  
    print sv1.dot(sv2)
    
