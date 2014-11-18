import sys
for line in sys.stdin:
    print '\t&\t'.join(line.strip().split())+'\t\\\\ \\hline'
