import sys
import codecs

fi = open(sys.argv[1], 'r', encoding='utf8')
fo = open(sys.argv[2], 'w', encoding='utf8')
entityCache = set()
entityLenFilter = 0
if len(sys.argv) > 3:
    entityLenFilter = int(sys.argv[3])
    for line in fi:
        entityStr = line[:line.index(' |||')]
        if (len(entityStr) <= entityLenFilter):
            entityCache.add(entityStr)
else:    
    for line in fi:
        entityStr = line[:line.index(' |||')]
        entityCache.add(entityStr)

entitySort = list(entityCache)
entitySort.sort(key = lambda s : len(s), reverse=True)
for eStr in entitySort:
    fo.write(eStr + '\n')

fi.close()
fo.close()
    

    
