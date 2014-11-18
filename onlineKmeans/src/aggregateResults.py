import sys
import json
delimiter = ','
keys = ["dataFileName", "n", "d", "k", "kTarget", "onlineCost", "kmppCost", "uniformCost"]
allRecords = [dict(json.loads(line.strip())) for line in sys.stdin]

#print delimiter.join([str(kv[0]) for kv in allRecords[0]])
#for record in allRecords: 
#    print delimiter.join([str(kv[1]) for kv in record])


fileNames = set([record["dataFileName"] for record in allRecords])

results  = {}
for record in allRecords:
    item  = (record["dataFileName"],record["kTarget"])
    if not item in results:
        results[item] = {"onlineCost":[], "kmppCost":[], "uniformCost":[],'k':[]}
    results[item]["n"] = record["n"]
    results[item]["d"] = record["d"]
    results[item]["k"].append(record["k"])
    results[item]["onlineCost"].append(record["onlineCost"])
    results[item]["kmppCost"].append(record["kmppCost"])
    results[item]["uniformCost"].append(record["uniformCost"])



header = ['dataFileName', 'kTarget', 'kmean', 'kmin','kmid','kmax','n', 'd', 'runs', 'onlineCost', 'kmppCost', 'uniformCost']
aggResults  = []
for (dataFileName, kTarget), costs in results.iteritems():
    aggResult = {}
    aggResult['dataFileName'] = dataFileName
    aggResult['kTarget'] = kTarget
    aggResult['n'] = costs['n']
    aggResult['d'] = costs['d']
    runs = len(costs["onlineCost"])
    aggResult['runs'] = runs
    ks = sorted(costs["k"])
    aggResult['kmin'] = ks[0]
    aggResult['kmid'] = ks[len(ks)/2]
    aggResult['kmax'] = ks[-1]
    aggResult['kmean'] = float(sum(ks))/float(len(ks))
    aggResult['onlineCost'] = float(sum(costs["onlineCost"]))/float(runs)
    aggResult['kmppCost'] = float(sum(costs["kmppCost"]))/float(runs)
    aggResult['uniformCost'] = float(sum(costs["uniformCost"]))/float(runs)
    aggResults.append(aggResult)
    
aggResultsList = [[res[h] for h in header] for res in aggResults]
aggResultsList.sort()
print delimiter.join(header)
for res in aggResultsList:
    print delimiter.join([str(x) for x in res]) 
    
    
    