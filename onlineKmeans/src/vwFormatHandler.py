import re, json
from numpy import zeros
from scipy.sparse import lil_matrix, csr_matrix
from sparseVector import SparseVector

class VWFormatHandler:
    def __init__(self):
        self._namespaceDelim = re.compile('\|')
        self._atLeastOneWhiteSpace = re.compile('\s+')
        
    def iterateRecords(self, lineIterator):
        featureToIndex = {}
        for line in lineIterator:
            #record = {}
            vwFormatVector = line.strip()
            namespaceSplit = self._namespaceDelim.split(vwFormatVector)
            if len(namespaceSplit) < 2:
                continue
            labelInfo = namespaceSplit[0].split()
            label = int(float(labelInfo[0]))
            weight = float(labelInfo[1]) if len(labelInfo) > 1 else 1.0
            tag = float(labelInfo[2]) if len(labelInfo) > 2 else ''
            labelTuple = (label,weight,tag)
            
            nameSpaces = namespaceSplit[1:] 
            features = {} 
            
            for nameSpace in nameSpaces:   
                nameSpaceParts = self._atLeastOneWhiteSpace.split(nameSpace,1)
                if len(nameSpaceParts) < 2: continue
                [namespaceName, namespaceFeaturesStr] = nameSpaceParts
                    
                namespaceFeatures = []
                for coordiante in namespaceFeaturesStr.split():
                    kv = coordiante.split(':')
                    if not kv[0] in featureToIndex:
                         featureToIndex[kv[0]] = len(featureToIndex)
                    key = featureToIndex[kv[0]]
                    value = float(kv[1]) if len(kv) > 1 else 1.0
                    namespaceFeatures.append((key,value))
                features[namespaceName] = namespaceFeatures
            yield (labelTuple,features)
            #sys.stdout.write('%s\n'%json.dumps((labelTuple,features)))
            
    def loadAsMatrixSlow(self, lineIterator):
        d = 0
        examples = []
        for example in self.iterateRecords(lineIterator):
            examples.append(example)
            for nameSpaceFeatures in example[1].itervalues():
                for (key,value) in nameSpaceFeatures:
                    d = max(d, key+1)
            #maxKey = max(max((kv[1] for kv in features) for features in example[1].itervalues()))
            #d = max(d, maxKey)
        n = len(examples)
        
        points = lil_matrix( (n,d) )
        for (i,example) in enumerate(examples):
            for nameSpaceFeatures in example[1].itervalues():
                for (key,value) in nameSpaceFeatures: 
                    points[i,key] = value
        return points
    
    
    def loadAsMatrix(self, lineIterator):
        maxKey = 0
        featureToIndex = {}
        examples = []
        for line in lineIterator:
            namespaceSplit = self._namespaceDelim.split(line.strip())
            if len(namespaceSplit) < 2:
                continue
            
            nameSpaces = namespaceSplit[1:] 
            example = []
            for nameSpace in nameSpaces:   
                nameSpaceParts = self._atLeastOneWhiteSpace.split(nameSpace,1)
                if len(nameSpaceParts) < 2: continue
                [_, namespaceFeaturesStr] = nameSpaceParts
                    
                for coordiante in namespaceFeaturesStr.split():
                    kv = coordiante.split(':')
                    if not kv[0] in featureToIndex:
                         featureToIndex[kv[0]] = len(featureToIndex)
                    key = featureToIndex[kv[0]]
                    value = float(kv[1]) if len(kv) > 1 else 1.0
                    example.append((key,value))
                    maxKey = max(maxKey,key)
            #examples.append(example)
            examples.append(example)
        d = maxKey
        points = [SparseVector(d, example) for example in examples]          
        return points

if __name__ == "__main__":
    import sys
    vwFormatHandler = VWFormatHandler()
    points = vwFormatHandler.loadAsMatrix(sys.stdin)
    #print points.shape
    