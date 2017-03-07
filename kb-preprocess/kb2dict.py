import sys
import codecs
import ast




def loadDictfromFile
    fi = open(sys.argv[1], 'r', encoding=encode)
    ast.literal_eval(fi.readline())





encode = 'utf8'

if len(sys.argv) >= 4:
    encode = sys.argv[3]

fi = open(sys.argv[1], 'r', encoding=encode)
fo = open(sys.argv[2], 'w', encoding='utf8')


kbDict={}
newEntityDic={}
i = 0
for line in fi:
    i += 1
    print('exporting the ' + str(i) + ' triple', end='\r', flush=True)
    entityStr = line[:line.index(' |||')]
    tmp = line[line.index('||| ') + 4:]
    relationStr = tmp[:tmp.index(' |||')]
    objectStr = tmp[tmp.index('||| ') + 4:].strip('\n')
    if entityStr not in kbDict:
        newEntityDic = {relationStr:objectStr}
        kbDict[entityStr] = newEntityDic
    else:
        kbDict[entityStr][relationStr] = objectStr


fo.write(str(kbDict))

fi.close()
fo.close()
    

    
