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

def main():
    for dataFileName in dataFileNames:
        vwFormatHandler = VWFormatHandler()
        f = open(rootDir + dataDirectory + dataFileName)
        points = vwFormatHandler.loadAsMatrix(f)
        f.close()
        normSquare = 0.0
        nnzs = 0
        d = 0
        for point in points:
            nnzs+=point.getNumNnz()
            normSquare+=point.getNormSquare()
            d = max(d,point.d)
        n = len(points)
        
        
        dataFileName = dataFileName.split('.')[0]
        sparse = "yes" if (n*d)/nnzs>=3 else "no"
        print '\t'.join(str(x) for x in [dataFileName.split('.')[0], nnzs, n, d, normSquare, sparse])    
if __name__ == '__main__':
    main()