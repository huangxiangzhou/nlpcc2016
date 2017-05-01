import sys
import codecs
import re
import json
import math
import Levenshtein


def countWord():
    fi = open('annotated_fb_data_train.txt','r',encoding='utf8')


    e2nDict = json.load(open('entity2name.lowcase.json','r',encoding='utf8'))

    print('e2nDict len:', len(e2nDict))

    oovTrain = set()

    countWord = {}
    for line in fi:
        lineTmp = line.strip().strip('?').lower()
        if len(lineTmp) == 0:
            continue

        tabIndex = lineTmp.index('\t')
        subject = lineTmp[:tabIndex].replace('www.freebase.com/','').replace('/','.')
        if subject in e2nDict:
            subject = e2nDict[subject]
        else:
            oovTrain.add(subject + '\n')
            subject = []
            
            
        lineTmp = lineTmp[tabIndex + 1:]
        tabIndex = lineTmp.index('\t')
        predicate = lineTmp[:tabIndex].replace('www.freebase.com/','')
        preLowerSet = set(re.split(r'_|/',predicate))

        lineTmp = lineTmp[tabIndex + 1:]
        tabIndex = lineTmp.index('\t')
        q = lineTmp[tabIndex + 1:]

        for sub in subject:
            if sub in q:
                q = q.replace(sub,'')
                break

        for pre in preLowerSet:
            q = q.replace(pre,'')

        wordSet = set(q.split(' '))
        for word in wordSet:
            if word not in countWord:
                    countWord[word] = 0
            
            countWord[word] += 1

    if '' in countWord:
        del countWord['']


    fo = open('countWord','w',encoding='utf8')

    for key in list(countWord):
        if countWord[key] < 1:
            del countWord[key]
        else:
            countWord[key] = math.log10(countWord[key])

    json.dump(countWord,fo)

    fo.close()


    fotxt = open('countWord.txt','w',encoding='utf8')

    for pair in sorted(countWord.items(), key=lambda d:d[1],reverse=True):
        fotxt.write(pair[0] + ':'+str(pair[1]) + '\n')


    fotxt.close()


    fooov = open('oovTrain.txt','w',encoding='utf8')

    oovstr = ''

    for s in oovTrain:
        oovstr += s
    fooov.write(oovstr.strip())

    fooov.close()

##
##countWord()

def loadKB(path, encode = 'utf8'):
        
    fi = open(path, 'r', encoding=encode)
    prePattern = re.compile(r'[·•\-\s]|(\[[0-9]*\])')


    kbDict={}
    newEntityDic={}
    i = 0
    for line in fi:
        i += 1
        print('exporting the ' + str(i) + ' triple', end='\r', flush=True)
        entityStr = line[:line.index(' |||')].strip()

        tmp = line[line.index('||| ') + 4:]
        relationStr = tmp[:tmp.index(' |||')].strip()
        relationStr, num = prePattern.subn('', relationStr)
        objectStr = tmp[tmp.index('||| ') + 4:].strip()
        if relationStr == objectStr: #delete the triple if the predicate is the same as object
            continue
        if entityStr not in kbDict:
            newEntityDic = {relationStr:objectStr}
            kbDict[entityStr] = []
            kbDict[entityStr].append(newEntityDic)
        else:
            kbDict[entityStr][len(kbDict[entityStr]) - 1][relationStr] = objectStr
            

    fi.close()

    
    return kbDict




def addAliasForKB(kbDictRaw):

    pattern = re.compile(r'[·•\-\s]|(\[[0-9]*\])')

    patternSub = re.compile(r'(\s*\(.*\)\s*)|(\s*（.*）\s*)')  # subject需按照 subject (Description) || Predicate || Object 的方式抽取, 其中(Description)可选

    patternBlank = re.compile(r'\s')

    patternUpper = re.compile(r'[A-Z]')

    patternMark = re.compile(r'《(.*)》')

    kbDict = kbDictRaw.copy()
    for key in list(kbDict):
        if patternSub.search(key):
            keyRe, num = patternSub.subn('', key)
            if keyRe not in kbDict:
                kbDict[keyRe] = kbDict[key]
            else:
                for kb in kbDict[key]:
                    kbDict[keyRe].append(kb)


    for key in list(kbDict):
        match = patternMark.search(key)
        if match:
            keyRe, num = patternMark.subn(r'\1', key)
            if keyRe not in kbDict:
                kbDict[keyRe] = kbDict[key]
            else:
                for kb in kbDict[key]:
                    kbDict[keyRe].append(kb)


    for key in list(kbDict):
        if patternUpper.search(key):
            keyLower = key.lower()
            if keyLower not in kbDict:
                kbDict[keyLower] = kbDict[key]
            else:
                for kb in kbDict[key]:
                    kbDict[keyLower].append(kb)

    for key in list(kbDict):
        if patternBlank.search(key):
            keyRe, num = patternBlank.subn('', key)
            if keyRe not in kbDict:
                kbDict[keyRe] = kbDict[key]
            else:
                for kb in kbDict[key]:
                    kbDict[keyRe].append(kb)
    
    return kbDict   


##print('Cleaning kb......')
##kbDictRaw = loadKB('nlpcc-iccpol-2016.kbqa.kb')
##kbDict = addAliasForKB(kbDictRaw)
##json.dump(kbDict, open('kbJson.cleanPre.alias.utf8','w',encoding='utf8'))
##print('\nDone!')



#把文本格式的word vector导出成Json格式供后续读入为Python的Dictionary
def convertToJson(inputPath='enwiki_300m20.txt', outputPath='vectorJson.utf8'\
                  ,encode = 'utf8'):
    fi = open(inputPath,'r',encoding=encode)

    ll = []
    for line in fi:
        ll.append(line.strip())
    listTmp = []

    embeddingDict = {}
    for i in range(len(ll)-1):
        lineTmp = ll[i+1]
        listTmp = []
        indexSpace = lineTmp.find(' ')
        embeddingDict[lineTmp[:indexSpace]] = listTmp
        lineTmp = lineTmp[indexSpace + 1:]
        for j in range(300):
            indexSpace = lineTmp.find(' ')
            listTmp.append(float(lineTmp[:indexSpace]))
            lineTmp = lineTmp[indexSpace + 1:]



    print('Vector size is ' + str(len(listTmp)))
    print('Dictionary size is ' + str(len(embeddingDict)))
            
    json.dump(embeddingDict,open(outputPath,'w',encoding=encode))
##
##print('Dumping word vector to Json format......')
##convertToJson()
##print('Done!')



#用训练数据训练答案模板
def getAnswerPatten(inputPath = 'annotated_fb_data_train.txt.map', outputPath = 'outputAP', e2nDictArg = {}):
    inputEncoding = 'utf8'
    outputEncoding = 'utf8'

    fi = open(inputPath, 'r', encoding=inputEncoding)
    fo = open(outputPath, 'w', encoding=outputEncoding)

    foov = open(outputPath+'.oov', 'w', encoding=outputEncoding)

    qRaw = ''

    APList = {}
    APListCore = {}

    if e2nDictArg == {}:
        e2nDict = json.load(open('entity2name.lowcase.json','r',encoding='utf8'))
    else:
        e2nDict = e2nDictArg

    print('e2nDict len:', len(e2nDict))

    for line in fi:
        lineTmp = line.strip().strip('?').lower()
        if len(lineTmp) == 0:
            continue

        tabIndex = lineTmp.index('\t')
        subject = lineTmp[:tabIndex].replace('www.freebase.com/','').replace('/','.')
        if subject in e2nDict:
            subject = e2nDict[subject]
        else:
            print(subject)
            subject = []
            
            
        lineTmp = lineTmp[tabIndex + 1:]
        tabIndex = lineTmp.index('\t')
        predicate = lineTmp[:tabIndex].replace('www.freebase.com/','')
        predicate = predicate.replace('/','.').replace('_',' ')

        lineTmp = lineTmp[tabIndex + 1:]
        tabIndex = lineTmp.index('\t')
        q = lineTmp[tabIndex + 1:]
        subFound = False
        for sub in subject:
            if sub in q:
                subIndex = q.find(sub)
                while subIndex != -1:
                    if q[subIndex-1] == ' ' or subIndex == 0: 
                        q = q.replace(sub,'(SUB)')
                        subFound = True
                        break
                    else:
                        subIndex = q.find(sub,subIndex+1)
                if subFound == True:
                    break
        if subFound == True:                    
            qt = q + ' ||| ' + predicate
            if qt not in APList:
                APList[qt] = 0
            APList[qt] += 1
        else:
            qt = q + ' ||| ' + str(subject) + '\t' +predicate + '\n'
            foov.write(qt)

    json.dump(APList, fo)
    foov.close()

    fotxt = open(outputPath+'.txt', 'w', encoding=outputEncoding)

    for key in APList:
        fotxt.write(key + ' ' + str(APList[key]) + '\n')
        
    fotxt.close()

    fi.close()    
    fo.close()
##
##print('Training answer pattern......')
##getAnswerPatten()
##print('Done!')


def indexAnswerPattenDict(oldDictPath='outputAP',outputPath = 'outputAP.index'):
    oldDict = json.load(open(oldDictPath,'r',encoding='utf8'))

    indexDict = {}
    for key in oldDict:
        splitIndex = key.index(' ||| ')
        qt = key[:splitIndex]
        pre = key[splitIndex+5:]
        if pre not in indexDict:
            indexDict[pre] = {}
        if qt not in indexDict[pre]:
            indexDict[pre][qt] = oldDict[key]

    json.dump(indexDict,open(outputPath,'w',encoding='utf8'))

    fotxt = open(outputPath+'.txt', 'w', encoding='utf8')

    for key in indexDict:
        fotxt.write(key + ' ' + str(indexDict[key]) + '\n')
        
    fotxt.close()

indexAnswerPattenDict()
   


def generateStemmingDict(inputPath = 'stemmer.txt', outputPath = 'stemmingDict'):
    inputEncoding = 'utf8'
    outputEncoding = 'utf8'

    distance = Levenshtein.ratio

    fi = open(inputPath, 'r', encoding=inputEncoding)
    fo = open(outputPath, 'w', encoding=outputEncoding)
    
    stemmingDict = {}
    
    for line in fi:
        if line.strip() == '':
            continue
        tmpList = line.strip().split(' => ')
        for word in tmpList[0].split(', '):
            if word not in stemmingDict:
                stemmingDict[word] = set()
            stemmingDict[word].add(tmpList[1])


    for key in stemmingDict:
        stemmingDict[key] = list(stemmingDict[key])
        for i in range(len(stemmingDict[key])):
            stemmingDict[key][i] = [stemmingDict[key][i],distance(stemmingDict[key][i],key)]


    json.dump(stemmingDict,fo)

    fi.close()
    fo.close()


    fotxt = open(outputPath+'.txt', 'w', encoding=outputEncoding)

    for key in stemmingDict:
        fotxt.write(key + ' ' + str(stemmingDict[key]) + '\n')
        
    fotxt.close()       
        

def appendWordNetStemmingDict(inputPath='stemmingDict.old', outputPath='stemmingDict',outputEncoding='utf8'):
    
    oldDict = json.load(open(inputPath,'r',encoding='utf8'))
    distance = Levenshtein.ratio
    fi = open('wordnet.map','r',encoding='utf8')
    fo = open(outputPath,'w',encoding='utf8')

    for m in list(oldDict):
        tmp = set()
        for l in list(oldDict[m]):
            tmp.add(l[0])
        oldDict[m] = set(tmp)
    
    for line in fi:
        m = line.strip().split(' ')
        if len(m) == 0:
            continue
        if m[0] not in oldDict:
            oldDict[m[0]]=set()
        oldDict[m[0]].add(m[1])

        
    for m in list(oldDict):
        oldDict[m] = list(oldDict[m])
        for i in range(len(oldDict[m])):
            if type(oldDict[m][i]) != str or type(m) != str:
                print(oldDict[m])
                input()
                continue
            oldDict[m][i] = [oldDict[m][i],distance(oldDict[m][i],m)]
    
    json.dump(oldDict,fo)




    fotxt = open(outputPath+'.txt', 'w', encoding=outputEncoding)

    for key in oldDict:
        fotxt.write(key + ' ' + str(oldDict[key]) + '\n')
        
    fotxt.close()               
    
##
##print('Dumping stemming mpping to json format......')
##generateStemmingDict()
##appendWordNetStemmingDict()
##print('Done!')


def extendN2EDict(n2eDict):
    n2eDictExt = {}
    print(len(n2eDict))
    for n in n2eDict:
        wList = n.split(' ')
        lenWList = len(wList)
        for i in range(lenWList):
            if wList[i] not in n2eDictExt:
                n2eDictExt[wList[i]] = []
            for e in n2eDict[n]:
                n2eDictExt[wList[i]].append([wList,e,i,lenWList - i])


    print(len(n2eDictExt))

    json.dump(n2eDictExt,open('n2eDictExt','w',encoding='utf8'))

    return n2eDictExt






        
