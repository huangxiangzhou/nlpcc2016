import sys
import codecs

fi = open(sys.argv[1], 'r', encoding='utf8')
fo = open(sys.argv[2], 'w', encoding='utf8')
objectCache = set()
for line in fi:
    tmp = line[line.index('||| ') + 4:]
    objectStr = tmp[tmp.index('||| ') + 4:]
    objectCache.add(objectStr)

objectSort = list(objectCache)
objectSort.sort(key = lambda s : len(s), reverse=True)
for oStr in objectSort:
    fo.write(oStr)

fi.close()
fo.close()
    

    
