import sys
import codecs

fi = open(sys.argv[1], 'r', encoding='utf8')
fo = open(sys.argv[2], 'w', encoding='utf8')
relationCache = set()
for line in fi:
    tmp = line[line.index('||| ') + 4:]
    relationStr = tmp[:tmp.index(' |||')]
    relationCache.add(relationStr)

relationSort = list(relationCache)
relationSort.sort(key = lambda s : len(s), reverse=True)
for rStr in relationSort:
    fo.write(rStr + '\n')

fi.close()
fo.close()
    

    
