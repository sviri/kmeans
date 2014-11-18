import sys
from random import random
#from numpy import sum
#from numpy.linalg import norm
from vectorList import VectorList
from numpy.random import randint

class KMeans:
    def __init__(self, points):
        self.points = points
        self.n = len(self.points)
        self.d = self.points[0].shape[1]
        self.mapping = None
        self.centers = None
        
    def initMappingKmeansPLusPLus(self, k):
        assert(k>=1)
        self.centers = VectorList(self.d)
        self.centers.append(self.points[randint(self.n)])
        minSquaredDistances = [self.centers[0].distSquare(point) for point in self.points]
        self.mapping = [0]*self.n
        
        for _ in xrange(k-1):
            index = self.reservoirSample(minSquaredDistances)
            newCenter = self.points[index]
            self.centers.append(newCenter)
            for i in xrange(self.n):
                minSquaredDistances[i] = min(minSquaredDistances[i], newCenter.distSquare(self.points[i]))
                
    def reservoirSample(self, weights):
        W = 0.0
        index = None
        for i,w in enumerate(weights):
            if w <= 0:
                continue
            W = W+w
            if random() <= w/W:
                index = i
        assert(index is not None)
        return index
    
    def initMappingOnline(self, k):
        self.centers = VectorList(self.d)
        kSwitch = k+10
        facilityCostDoublingTriger = k
        facilityCostDoublingFactor = 10.0
        centersAddedInThisPhase = 0
        for i,point in enumerate(self.points):
            if len(self.centers) < kSwitch:
                self.centers.append(point)
                if len(self.centers) == kSwitch:
                    minInnerClusterDistances = kSwitch + 2*(kSwitch - k)
                    allSquaredDistances = []
                    for vector in self.centers.getVectors():
                        squaredDistances = self.centers.computeSquaredDistances(vector)
                        allSquaredDistances.extend(squaredDistances)
                    allSquaredDistances.sort()
                    facilityCost = sum(allSquaredDistances[:minInnerClusterDistances])/2.0                
            else:
                # Main phase
                (minIndex, minSquaredDistance) = self.centers.minIndexAndSquaredDistance(point)
                p = min(minSquaredDistance/facilityCost,1.0)
                if random() < p:
                    self.centers.append(point)
                    centersAddedInThisPhase+=1
                if centersAddedInThisPhase > facilityCostDoublingTriger:
                    facilityCost = facilityCost*facilityCostDoublingFactor
                    centersAddedInThisPhase = 0
    
    def initMappingUniformRandomCenters(self, k):
        self.centers = VectorList(self.d)
        for _ in xrange(k):
            self.centers.append(self.points[randint(self.n)])


    def costOfCenters(self):
        cost = 0.0
        for i in xrange(self.n):
            (_,distSquared) = self.centers.minIndexAndSquaredDistance(self.points[i])
            cost+=distSquared
        return cost

    def getNumberOfClusters(self):
        return len(self.centers)
            
if __name__ == "__main__":
    import sys
    from vwFormatHandler import VWFormatHandler 
    
    #getting some test points
    vwFormatHandler = VWFormatHandler()
    rootDir = "/Users/edo/Documents/Papers/onlineKmeans/"
    dataFileName = rootDir + "data/magic04.vw"
    n = 100
    lines = []
    f = open(dataFileName)
    for _ in xrange(n):
        lines.append(f.readline())
    f.close()
    points = vwFormatHandler.loadAsMatrix(lines)

    # starting the test
    print "finished loading"
    k = 10
    km = KMeans(points)
        
    print "running online K means"
    km.initMappingOnline(k)
    onlineCost = km.costOfCenters()
    k2 = km.getNumberOfClusters()
    
    print "running K means ++"
    km.initMappingKmeansPLusPLus(k2)
    kmppCost = km.costOfCenters()
    

    print "running uniform random centers"
    km.initMappingUniformRandomCenters(k2)
    randCost = km.costOfCenters()
    
    print "test data at: %s"%dataFileName
    print "number of points = %d"%n
    print "number of clusters = %d"%k2
    print "online k means cost = %.3E"%onlineCost
    print "k means++ cost = %.3E"%kmppCost
    print "uniform random centers  cost = %.3E"%randCost
    
    print "test passed"