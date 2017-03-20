import sys
import codecs
import re


def loadKB(path, encode = 'utf16'):
        
    fi = open(path, 'r', encoding=encode)
    pattern = re.compile(r'[·•\-\s]|(\[[0-9]*\])')

    kbDict={}
    newEntityDic={}
    i = 0
    for line in fi:
        i += 1
        print('exporting the ' + str(i) + ' triple', end='\r', flush=True)
        entityStr = line[:line.index(' |||')].lower().strip().replace(' ', '')
        tmp = line[line.index('||| ') + 4:]
        relationStr = tmp[:tmp.index(' |||')].lower().strip().replace(' ', '')
        relationStr, num = pattern.subn('', relationStr)
        objectStr = tmp[tmp.index('||| ') + 4:].strip('\n').lower().replace(' ', '')
        if entityStr not in kbDict:
            newEntityDic = {relationStr:objectStr}
            kbDict[entityStr] = []
            kbDict[entityStr].append(newEntityDic)
        else:
            kbDict[entityStr][len(kbDict[entityStr]) - 1][relationStr] = objectStr
        #查找别名
        if (relationStr[len(relationStr) - 1:] == '名' or relationStr[len(relationStr) - 2:] == '名字' or relationStr[len(relationStr) - 2:] == '名称') \
           and objectStr.strip() != entityStr:
            oStrip = objectStr.strip()
            if oStrip not in kbDict:
                kbDict[oStrip] = []
            kbDict[oStrip].append(newEntityDic)
            

    fi.close()
    return kbDict


    
