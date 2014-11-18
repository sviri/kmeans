import sys
import json
import time
import socket
from kmeans import KMeans
from vwFormatHandler import VWFormatHandler
import itertools

rootDir = '/Users/edo/Documents/Papers/onlineKmeans/'
if socket.gethostname() == 'lickedpredict.corp.ne1.yahoo.com':
    rootDir = '/home/edo/kmeans/'
dataDirectory = 'data/'
outDirectory = 'out/'

dataFileNames = ['20news-binary.vw',\
                 'adult.vw', \
                 'covtype.vw',\
                 'ijcnn1.vw',\
                 'kddcup04_phy.vw',\
                 'letter.vw',\
                 'magic04.vw',\
                 'maptaskcoref.vw',\
                 'nomao.vw',\
                 'poker.vw',\
                 'shuttle.binary.vw',\
                 'skin.vw',\
                 'vehv2binary.vw',\
                 'w8all.vw']


def iteratorStopper(iterator, stopIndex):
    for index, item in enumerate(iterator):
        if index >= stopIndex:
            return
        yield item

def main():
    kTargets = range(1,10,1)# + range(10,101,10)
    rounds = range(3)
    #for maxn in [100*(2**i) for i in xrange(16)]:   
    for dataFileName in dataFileNames:
        print dataFileName
        
        vwFormatHandler = VWFormatHandler()
        f = open(rootDir + dataDirectory + dataFileName)
        
        print "Started loading data..."
        
        #points = vwFormatHandler.loadAsMatrix(iteratorStopper(f,maxn))
        points = vwFormatHandler.loadAsMatrix(f)
        print "Finished loading data."
        f.close() 
        d = points[0].shape[1]
        n = len(points)
        
        for round in rounds:
            for kTarget in kTargets:
                try:
                    km = KMeans(points)
                    # Online
                    print "running online k means, round %d, n = %d, target k = %d"%(round,n,kTarget)
                    km.initMappingOnline(kTarget)
                    onlineCost = km.costOfCenters()
                    k = km.getNumberOfClusters()
                    
                    # K means ++
                    print "running k means++, round %d, n = %d, target k = %d"%(round,n,k)
                    km.initMappingKmeansPLusPLus(k)
                    kmppCost = km.costOfCenters()    
                  
                    # Uniform random centers
                    print "running uniform random, round %d, n = %d, target k = %d"%(round,n,k)
                    km.initMappingUniformRandomCenters(k)
                    uniformCost = km.costOfCenters()
           
                    timeStr = time.strftime('%Y_%m_%d_%H_%M')
                    resultsFileName = rootDir + outDirectory + "results_" + timeStr + '.json' 
                    
                    rf = open(resultsFileName,'a+')
                    record = [('dataFileName',dataFileName),('n',n),('d',d),('k',k),('kTarget',kTarget),\
                              ('onlineCost',onlineCost),\
                              ('kmppCost',kmppCost),\
                              ('uniformCost',uniformCost)]
                    
                    rf.write('%s\n'%json.dumps(record))
                    rf.close()
                except:
                    pass
        
if __name__ == '__main__':
    main()