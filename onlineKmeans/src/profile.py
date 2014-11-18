import sys
import cProfile, pstats, StringIO
#import runKMeansExperiments
from vwFormatHandler import VWFormatHandler
from kmeans import KMeans


print "=========== START PREPROCESSING =============="
vwFormatHandler = VWFormatHandler()
file =open('/Users/edo/Documents/Papers/onlineKmeans/data/20news-binary.vw')

n = 10000
lines = []
for i,line in enumerate(file):
    lines.append(line)
    if i > n:
        break
file.close()
points = vwFormatHandler.loadAsMatrix(lines)
km = KMeans(points)

print "=========== END PREPROCESSING =============="

pr = cProfile.Profile()
pr.enable()

print "=========== START PROFILING =============="



km.initMappingOnline(5)
    

'''
for point in points:
    dotProduct = point.dot(point.transpose())[0,0]
'''

    
print "=========== END PROFILING ============="

    
pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()