from numpy import zeros, array
from numpy.linalg import norm
from scipy.sparse import csr_matrix

class VectorList:
    def __init__(self, d, initLength=0):
        self.d = d
        self._vectors = []
        self._normsSquared = []
        self._length = 0
        
    def __len__(self):
        return self._length

    def append(self, vector):
        assert(vector.shape == (1,self.d))
        self._vectors.append(vector)
        self._normsSquared.append(sum(x**2 for x in vector.data))
        self._length = len(self._vectors) 
        
    def __setitem__(self, i, vector):
        assert(vector.shape == (1,self.d)) 
        self._vectors[i] = vector
        self._normsSquared[i] = sum(x**2 for x in vector.data)
        
    def __getitem__(self, i):
        return self._vectors[i]
    
    def computeSquaredDistances(self, vector):
        return [v.distSquare(vector) for v in self._vectors]

    def minIndexAndSquaredDistance(self, vector):
        squaredDistances = self.computeSquaredDistances(vector)
        return min(enumerate(squaredDistances), key=lambda item:item[1])
    
    def getVectors(self):
        return self._vectors
