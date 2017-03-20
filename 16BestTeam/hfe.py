import codecs
import sys
import json
import re



def removeHFE(kbDict,hfePath='hfe.utf8',encode='utf8'):
    hfe = json.load(open(hfePath,'r',encoding=encode))
    kbDictCopy = kbDict.copy()
    for key in hfe:
        del kbDictCopy[key]
    return kbDictCopy


    
def generateHighFreqEntityList(lKey,inputPath = 'trainingAndTestingQ.utf8',\
                               outputPath = 'hfe',encode='utf8',threshold = 150):

    fi=open(inputPath,'r',encoding=encode)

    fo=open(outputPath+'.'+encode,'w',encoding=encode)

    fo2=open(outputPath+'.txt','w',encoding=encode)

    entityCount = {}
    listQ = []
    qStrAll = ''
    for line in fi:
        qStrAll += line

    i = 0
    for key in lKey:
        try:
            pattern = re.compile(r''+key.replace('\\','\\\\').replace('?','\?')\
                                 .replace('(','\(').replace(')','\)').replace('^','\^')\
                                 .replace('.','\.').replace('$','\$').replace('|','\|')\
                                 .replace('*','\*').replace('+','\+')\
                                 .replace('[','\[').replace(']','\]'))
        except Exception:
            print(key)
        entityCount[key] = len(pattern.findall(qStrAll))
        i += 1
        print(str(i),end='\r',flush=True)

    hfe = {}

    for key in entityCount:
        count = entityCount[key]
        if count > threshold:
            hfe[key] = count

    json.dump(hfe,fo)

    for key in hfe:
        fo2.write(key + ' ||| ' + str(hfe[key]) + '\n')

    fi.close()
    fo.close()
    fo2.close()
    
        
