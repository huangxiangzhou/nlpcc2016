import sys
import codecs
import lcs   #the lcs module is in extension folder
import time
import json
import re
import Levenshtein



class answerCandidate:
    def __init__(self, sub = ['',''], pre = '', qRaw = '', score = 0, kbDict = [], wS = 1, wP = 10, wAP = 1):
        self.sub = sub[0]
        self.entity = sub[1]
        self.pre = pre     
        self.qRaw = qRaw     
        self.score = score
        self.kbDict = kbDict
        self.origin = ''
        self.scoreDetail = [0,0,0,0,0]
        self.wS = wS
        self.wP = wP
        self.wAP = wAP
        self.scoreSub = 0
        self.scoreAP = 0
        self.scorePre = 0
        self.qt = []
        self.preCount = 0
        self.entityCount = []
        

    def calcScore(self, qtList, countCharDict, debug=False, includingObj = [], vectorDict = {}, stemmingDict = {}, matchQt = False):


        distance = Levenshtein.ratio
        scoreAP = 0
        q = self.qRaw
        scoreSub = 0

        pre = self.pre
        scorePre = 0
        sub = ''
        if type(self.sub) == str:
            sub = self.sub
            subSplit = self.sub.split(' ')
            if sub in q:   
                for w in subSplit:
                    if w in countCharDict:
                        scoreSub += 1/(countCharDict[w] + 1)
                    else:
                        scoreSub += 1
            else:
                subSet = set(subSplit)
                qSet = set(q.split(' '))
                for w in (subSet & qSet):
                    if w in countCharDict:
                        scoreSub += 1/(countCharDict[w] + 1)
                    else:
                        scoreSub += 1
                if len(subSet) != 0:
                    scoreSub = scoreSub/len(subSet)
                

        if type(self.sub) == list:
            for s in self.sub[0]:
                sub += s + ' '
            sub = sub.strip()

        
        
        qtKey = q.replace(sub,'(SUB)',1)
        

        qWithoutSub = q.replace(sub,'').replace('  ', ' ').strip()

        qWithoutSubSet = set(qWithoutSub.split(' '))

        qWithoutSub = list(qWithoutSubSet)
        qWithoutSubSet = set()

        for i in range(len(qWithoutSub)):
            if qWithoutSub[i] in stemmingDict:
                qWithoutSub[i] = stemmingDict[qWithoutSub[i]][0][0]
            qWithoutSubSet.add(qWithoutSub[i])

        lastPreIndex = pre.rfind('.')
        if lastPreIndex != -1:
            preLowerSet = set(re.split(r' |\.',pre[lastPreIndex+1:]))
        else:
            preLowerSet = set(re.split(r' |\.',pre))

        preLower = list(preLowerSet)
        preLowerSet = set()

        for i in range(len(preLower)):
            if preLower[i] in stemmingDict:
                preLower[i] = stemmingDict[preLower[i]][0][0]
            preLowerSet.add(preLower[i])


        maxIntersection = qWithoutSubSet & preLowerSet



        preFactor = 0
        for char in maxIntersection:
            if char in countCharDict:
                preFactor += 1/(countCharDict[char] + 1)
            else:
                preFactor += 1

        
        if len(maxIntersection) == 0:
            for w1 in qWithoutSubSet:
                for w2 in preLowerSet:
                    if w1 == '' or w2 == '' or w1[0] != w2[0]:
                        continue
                    div = 1
                    if w1 in countCharDict:
                        div = countCharDict[w1] + 1
                    dWord = distance(w1,w2) / div
                    if preFactor < dWord:
                        preFactor = dWord
            


        if len(pre) != 0:
            scorePre = preFactor / len(qWithoutSubSet | preLowerSet)
        else:
            scorePre = 0

        
        if len(includingObj) != 0 and scorePre == 0:
            for objStr in includingObj:
                scorePreTmp = 0
                preLowerSet = set(objStr.lower())
                intersection1 = qWithoutSubSet1 & preLowerSet
                intersection2 = qWithoutSubSet2 & preLowerSet

                if len(intersection1) > len(intersection2):
                    maxIntersection = intersection1
                else:
                    maxIntersection = intersection2

                preFactor = 0
                for char in maxIntersection:
                    if char in countCharDict:
                        preFactor += 1/(countCharDict[char] + 1)
                    else:
                        preFactor += 1

                scorePreTmp = preFactor / len(qWithoutSubSet | preLowerSet)
                if scorePreTmp > scorePre:
                    scorePre = scorePreTmp

        if len(vectorDict) != 0 and len(pre) != 0:

            scorePre = 0
            
            segListPre = []
            
            lenPre = len(pre)

            lenPreSum = 0
            for i in range(lenPre):
                for j in range(lenPre):
                    if i+j < lenPre:
                        preWordTmp = pre[i:i+j+1]
                        if preWordTmp in vectorDict:
                            segListPre.append(preWordTmp)
                            lenPreSum += len(preWordTmp)
                
            
            lenQNS = len(qWithoutSub)
            segListQNS = []
            for i in range(lenQNS):
                for j in range(lenQNS):
                    if i+j < lenQNS:
                        QNSWordTmp = qWithoutSub[i:i+j+1]
                        if QNSWordTmp in vectorDict:
                            segListQNS.append(QNSWordTmp)


            
            for preWord in segListPre:
                scoreMaxCosine = 0
                for QNSWord in segListQNS:
                    cosineTmp = lcs.cosine(vectorDict[preWord],vectorDict[QNSWord])
                    if cosineTmp > scoreMaxCosine:
                        scoreMaxCosine = cosineTmp
                scorePre += scoreMaxCosine * len(preWord)

            if lenPreSum == 0:
                scorePre = 0
            else:
                scorePre = scorePre / lenPreSum
            

            self.scorePre = scorePre            

        



        if type(self.sub) == list:
            if len(self.sub[0]) == len(self.sub[1]):
                lenSub = len(self.sub[0])
                for i in range(lenSub):
                    w = self.sub[0][i]
                    wC = self.sub[1][i]
                    if w in countCharDict:
                        scoreSub += 1/(countCharDict[w] + 1)*distance(w,wC)
                    else:
                        scoreSub += 1*distance(w,wC)
                scoreSub = scoreSub / lenSub
                    
            else:
                subIntersaction = set(self.sub[0]) & set(self.sub[1])
                scoreSub = len(subIntersaction) / len(set(self.sub[0]) | set(self.sub[1]))

                

        self.scoreSub = scoreSub
        self.scorePre = scorePre

##        if debug and len(maxIntersection) != 0:
##            print(qWithoutSubSet,preLowerSet,maxIntersection,preFactor)
##            print(scoreSub,scorePre,scoreAP)

        
        if pre in qtList:
            if qtKey in qtList[pre]:
                scoreAP = qtList[pre][qtKey]
            else:
                for qt in qtList[pre]:
                    scoreMatch = distance(qt, qtKey)
##                    qtSet = set(qt.split(' '))
##                    qtKeySet = set(qtKey.split(' '))
##                    scoreMatch = len(qtSet & qtKeySet)/(len(qtSet | qtKeySet))
                    if scoreMatch > scoreAP:
                        scoreAP = scoreMatch
                        self.qt = qt
        else:
            scoreAP = 0
                    
        self.scoreAP = scoreAP


        self.score = scoreSub * 1 + scorePre * 6.8 + scoreAP * 5.0
        
        return self.score

def getAnswer(sub, pre, kbDict):
    answerList = []
    for kb in kbDict[sub]:
        if pre in kb:
            answerList.append(kb[pre])
   
    return answerList

    



def answerQ (qRaw, n2eDict, kbDict, qtList, countCharDict, stemmingDict, vectorDict, entityCountDict = {}, n2eDictExt = {},wP=10, wAP =1,threshold=0, debug=False):
    q = qRaw.strip().lower().strip('?')
    
    candidateSet = set()
    
    result = ''

 
    maxScore = 0

    bestAnswer = set()


    # Get N-Gram set of the question
##    qWordList = re.split(r' |\'s',pre)
##    
##
##    while '' in qWordList:
##        for i in range(len(qWordList)):
##            if qWordList[i] == '':
##                qWordList = qWordList[:i] + qWordList[i+1:]
##                break
    qWordList = q.split(' ')

    if len(n2eDictExt) == 0:

        nGramSet = set()
        for i in range(len(qWordList)):
            for j in range(len(qWordList) - i):
                strTmp = ''
                for w in qWordList[i:i+j+1]:
                    strTmp += w + ' '
                nGramSet.add(strTmp.strip())

        for strNGram in list(nGramSet):
            if '\'s' in strNGram:
                if strNGram.index('\'s') == len(strNGram) - 2:
                    nGramSet.add(strNGram[:-2])
                    


        # Get all the candidate triple

        candidateSubject = {}
        maxNGramLen = 0
        for nGram in nGramSet:
            if nGram in n2eDict:
                if maxNGramLen < len(nGram):
                    maxNGramLen = len(nGram)
                candidateSubject[nGram] = []
                for sub in n2eDict[nGram]:
                    candidateSubject[nGram].append(sub)


        for nGram in candidateSubject:
            for sub in candidateSubject[nGram]:
                if sub in kbDict:
                    for pre in kbDict[sub]:
                        newAnswerCandidate = answerCandidate([nGram, sub], pre, q, wP=wP,wAP=wAP)
                        candidateSet.add(newAnswerCandidate)
                    
    else:
        nGramSet = set()
        qWordSet = set()
        candidateSubject = {}
        for i in range(len(qWordList)):
            qWord = qWordList[i]
            if qWord in n2eDictExt:
                for pair in n2eDictExt[qWord]:
                    entity = pair[1]
                    subEntity = pair[0]
                    subQ = qWordList[i - pair[2]:i + pair[3]]
                    if entity in kbDict:
                        for pre in kbDict[entity]:
                            newAnswerCandidate = answerCandidate([[subQ,subEntity], entity], pre, q, wP=wP,wAP=wAP)
                            candidateSet.add(newAnswerCandidate)

            
            if '\'s' in qWord:
                if qWord.index('\'s') == len(qWord) - 2:
                    qWord = qWord[:-2]
                    if qWord in n2eDictExt:
                        for pair in n2eDictExt[qWord]:
                            entity = pair[1]
                            subEntity = pair[0]
                            subQ = qWordList[i - pair[2]:i + pair[3]]
                            if entity in kbDict:
                                for pre in kbDict[entity]:
                                    newAnswerCandidate = answerCandidate([[subQ,subEntity], entity], pre, q, wP=wP,wAP=wAP)
                                    candidateSet.add(newAnswerCandidate)


                    

##    for name in n2eDict:
##        lcsLen = len(lcs.lcs(name,q))
##        if lcsLen > maxNGramLen:
##            candidateSubject[name] = []
##            for sub in n2eDict[name]:
##                candidateSubject[name].append(sub) 


    if debug == True:
        print('Size of nGramSet: ', len(nGramSet))
        for nGram in nGramSet:
            print(nGram)
        print('Size of candidateSubject: ', len(candidateSubject))
        for sub in candidateSubject:
            print(sub)


        

   
    
    
##    candidateSetCopy = candidateSet.copy()
##    if debug:
##        print('len(candidateSet) = ' + str(len(candidateSetCopy)), end = '\r', flush=True)
##    candidateSet = set()
##
##    candidateSetIndex = set()
##
##    for aCandidate in candidateSetCopy:
##        strTmp = str(aCandidate.sub+'|'+aCandidate.pre)
##        if strTmp not in candidateSetIndex:
##            candidateSetIndex.add(strTmp)
##            candidateSet.add(aCandidate)

    #print(str(len(candidateSet)))
    bestScorePre = 0
    for aCandidate in candidateSet:
        scoreTmp = aCandidate.calcScore(qtList, countCharDict, debug, stemmingDict = stemmingDict,matchQt = False)
        if scoreTmp > maxScore:
            maxScore = scoreTmp
            bestAnswer = set()
            bestScorePre = 0
        if scoreTmp == maxScore:
            if bestScorePre < aCandidate.scorePre:
                bestScorePre = aCandidate.scorePre                
            bestAnswer.add(aCandidate)

    for answer in bestAnswer:
        answer.preCount = len(kbDict[answer.entity])
        if answer.entity in entityCountDict:
            answer.entityCount = entityCountDict[answer.entity]

##    if bestScorePre == 0:
##        bestAnswerCopy = bestAnswer.copy()
##        for aCandidate in candidateSet:
##            scoreTmp = aCandidate.calcScore(qtList, countCharDict, debug, stemmingDict = stemmingDict, matchQt = True)
##            if scoreTmp > maxScore:
##                maxScore = scoreTmp
##                bestAnswer = set()
##            if scoreTmp == maxScore:              
##                bestAnswer.add(aCandidate)        
            

##    bestAnswerCopy = bestAnswer.copy()
##    for aCandidate in bestAnswerCopy:
##        if aCandidate.score == aCandidate.scoreSub:
##            scoreReCal = aCandidate.calcScore(qtList, countCharDict,debug, includingObj=getAnswer(aCandidate.sub, aCandidate.pre, kbDict))
##            if scoreReCal > maxScore:
##                bestAnswer = set()
##                maxScore = scoreReCal
##            if scoreReCal == maxScore:
##                bestAnswer.add(aCandidate)


            
##    bestAnswerCopy = bestAnswer.copy()
##    bestAnswer = set()
##    for aCandidate in bestAnswerCopy:
##        aCfound = 0
##        for aC in bestAnswer:
##            if aC.pre == aCandidate.pre and aC.sub == aCandidate.sub:
##                aCfound = 1
##                break
##        if aCfound == 0:
##            bestAnswer.add(aCandidate)


##    bestAnswerCopy = bestAnswer.copy()
##    for aCandidate in bestAnswerCopy:
##        if aCandidate.score == aCandidate.scoreSub:
##            scoreReCal = aCandidate.calcScore(qtList, countCharDict,debug, includingObj=getAnswer(aCandidate.sub, aCandidate.pre, kbDict))
##            if scoreReCal > maxScore:
##                bestAnswer = set()
##                maxScore = scoreReCal
##            if scoreReCal == maxScore:
##                bestAnswer.add(aCandidate)
##
##
##    bestAnswerCopy = bestAnswer.copy()
##    if len(bestAnswer) > 1: # use word vector to remove duplicated answer
##        for aCandidate in bestAnswerCopy:
##            scoreReCal = aCandidate.calcScore(qtList, countCharDict,debug, includingObj=getAnswer(aCandidate.sub, aCandidate.pre, kbDict), vectorDict=vectorDict)
##            if scoreReCal > maxScore:
##                bestAnswer = set()
##                maxScore = scoreReCal
##            if scoreReCal == maxScore:
##                bestAnswer.add(aCandidate)
            
            
    if debug:
        for ai in bestAnswer:
            print(ai.sub,ai.scoreSub,ai.pre,ai.scorePre,ai.qt,ai.scoreAP)

    return bestAnswer
        


def loadQtList(path, encode = 'utf8'):
    qtList = json.load(open(path,'r',encoding=encode))

    return qtList

def loadcountCharDict(path, encode = 'utf8'):
    countCharDict = json.load(open(path,'r',encoding=encode))

    return countCharDict

def loadvectorDict(path, encode = 'utf8'):
    vectorDict = json.load(open(path,'r',encoding=encode))

    return vectorDict  

def answerAllQ(pathInput, pathOutput, n2eDict, kbDict, qtList, countCharDict, stemmingDict, vectorDict, entityCountDict ={},n2eDictExt = {},qIDstart=1, wP=10, wAP = 1):
    fq = open(pathInput, 'r', encoding='utf8')
    timeStart = time.time()
    fo = open(pathOutput, 'w', encoding='utf8')
    fo.close()

    fowrong = open(pathOutput+'wrong', 'w', encoding='utf8')
    fowrong.close()

    fowrongAP = open(pathOutput+'wrongAP', 'w', encoding='utf8')
    fowrongAP.close()

    fofoundAP = open(pathOutput+'foundAP', 'w', encoding='utf8')
    fofoundAP.close()
    foww = open(pathOutput+'wrongSP', 'w', encoding='utf8')
    foww.close()

    fofw = open(pathOutput+'foundSP', 'w', encoding='utf8')
    fofw.close()

    foroom = open(pathOutput+'room', 'w', encoding='utf8')
    foroom.close()


    
    listQ = []
    goldenSP = []
    count1 = 0
    count1S = 0
    countN = 0
    roomRest = 0
    for line in fq:
        if line[0] == 'm':
            qIndex = line.index('\tQ: ')
            listQ.append(line[qIndex+4:].strip())
            goldenSP.append(line[:qIndex])

    correctSub = 0
    for i in range(len(listQ)):
        q = listQ[i]
        goldenPre = goldenSP[i][goldenSP[i].index(' ||| ')+5:]
        goldenEntity = goldenSP[i][:goldenSP[i].index(' : ')]
        goldenSubList = goldenSP[i][goldenSP[i].index(' : ')+3:goldenSP[i].index(' ||| ')]

        result = answerQ(q, n2eDict, kbDict, qtList, countCharDict, stemmingDict, vectorDict, entityCountDict =entityCountDict,n2eDictExt = n2eDictExt,wP=wP,wAP =wAP)

        answerfoundCount = 0
        answerStr = ''
        scoreAPCount = 0
        goldenSub = ''
        
        if len(result) == 0:
            answerStr = 'No answer found!\n'
        for res in result:
            if res.scoreAP >= 1:
                scoreAPCount += 1
            if res.entity == goldenEntity and res.pre.replace(' ','_') == goldenPre:
                goldenSub = res.sub
                answerfoundCount += 1
            answerStr += res.entity + ' : ' + str(res.sub) + ' \t||| '+str(res.entityCount)+' ||| ' + res.pre.replace(' ','_')+ '\t'\
                         + str(res.score)+ '\t' + str(res.scoreSub)+ '\t' + str(res.scorePre)+ '\t' + str(res.scoreAP) + '\n'

        preG = goldenPre.replace('_',' ')
        scoreGoldenMax = 0
        goldenAnswerSelected = ''
        for nGram in eval(goldenSubList):
            goldenAnswer = answerCandidate([nGram, goldenEntity], preG, q.strip().lower().strip('?'), wP=wP,wAP=wAP)
            scoreGolden = goldenAnswer.calcScore(qtList, countCharDict, False, stemmingDict = stemmingDict,matchQt = False)
            if scoreGoldenMax < scoreGolden:
                scoreGoldenMax = scoreGolden
                goldenAnswerSelected = goldenAnswer
        

        roomMark = False
        correctSub += 1
        for res in result:
            if res.sub != goldenSub and res.scoreAP == 0:
                correctSub -= 1
                roomMark = True
                break


        if answerfoundCount > 0:
            if answerfoundCount == len(result):
                count1S += 1
            if len(result) == 1:
                mark = 'Right'
                count1 += 1
            else:
                mark = 'Found'
                countN += 1
        else:
            mark = 'Wrong'


        goldenStr = goldenSP[i]+ '\n'
        if type(goldenAnswerSelected) != str:
            goldenStr = goldenSP[i]+ '\t'+str(goldenAnswerSelected.score)+ '\t' + str(goldenAnswerSelected.scoreSub)+ '\t' + str(goldenAnswerSelected.scorePre)+ '\t' + str(goldenAnswerSelected.scoreAP) +'\n'
        fo = open(pathOutput, 'a', encoding='utf8')
        fo.write(str(i+1)+ '\t' + mark +'\t: '+q+'\n')
        fo.write(goldenStr)
        fo.write(answerStr)

        
        if mark == 'Found':
            if scoreAPCount > 0:
                fofoundAP = open(pathOutput+'foundAP', 'a', encoding='utf8')
                fofoundAP.write(str(i+1)+ '\t' + mark +'\t: '+q+'\n')
                fofoundAP.write(goldenStr)
                fofoundAP.write(answerStr)
                fofoundAP.close()
            else:
                fofw = open(pathOutput+'foundSP', 'a', encoding='utf8')
                fofw.write(str(i+1)+ '\t' + mark +'\t: '+q+'\n')
                fofw.write(goldenStr)
                fofw.write(answerStr)
                fofw.close()
                roomRest += 1

        if roomMark == True:           
            foroom = open(pathOutput+'room', 'a', encoding='utf8')
            foroom.write(str(i+1)+ '\t' + mark +'\t: '+q+'\n')
            foroom.write(goldenStr)
            foroom.write(answerStr)
            foroom.close()

        

        if mark == 'Wrong':           
            fowrong = open(pathOutput+'wrong', 'a', encoding='utf8')
            fowrong.write(str(i+1)+ '\t' + mark +'\t: '+q+'\n')
            fowrong.write(goldenStr)
            fowrong.write(answerStr)
            fowrong.close()
            if scoreAPCount > 0:
                fowrong = open(pathOutput+'wrongAP', 'a', encoding='utf8')
                fowrong.write(str(i+1)+ '\t' + mark +'\t: '+q+'\n')
                fowrong.write(goldenStr)
                fowrong.write(answerStr)
                fowrong.close()
            else:
                foww = open(pathOutput+'wrongSP', 'a', encoding='utf8')
                foww.write(str(i+1)+ '\t' + mark +'\t: '+q+'\n')
                foww.write(goldenStr)
                foww.write(answerStr)
                foww.close()
                roomRest += 1

            
        
        print('processing ' + str(i + 1) + 'th Q.\tAv time cost: ' + str((time.time()-timeStart) / (i+1))[:6] + ' sec', end = '\r', flush=True)
        fo.close()


    accuracy1 = count1 / len(listQ)
    accuracy1S = count1S / len(listQ)
    accuracyN = (count1 + countN) / len(listQ)
    print('\nAccuracy1 : ',accuracy1)
    print('Accuracy1S : ',accuracy1S)
    print('AccuracyN : ',accuracyN)
    print('RoomRest : ',roomRest,roomRest/len(listQ))

    print('correctSub :',correctSub,correctSub/len(listQ))
    fo = open(pathOutput, 'a', encoding='utf8')
    fo.write('\n\nMetric')
    fo.write('\nAccuracy1 : '+str(accuracy1))
    fo.write('\nAccuracy1S : '+str(accuracy1S))
    fo.write('\nAccuracyN : '+str(accuracyN))
    fo.write('RoomRest : '+str(roomRest)+' ' +str(roomRest/len(listQ)))
    fo.close()
    fq.close()
    return roomRest/len(listQ)
    

def loadResAndanswerAllQ(pathInput, pathOutput, pathn2eDict, pathDict, pathQt, pathCD, pathSD, pathVD, encode='utf8', qIDstart=1, wP=10,wAP =1):
    print('Start to load n2eDict from json format file: ' + pathn2eDict)
    n2eDict = json.load(open(pathn2eDict, 'r', encoding=encode))
    print('Loaded n2eDict completely! kbDic length is '+ str(len(n2eDict)))
    print('Start to load kbDict from json format file: ' + pathDict)
    kbDict = json.load(open(pathDict, 'r', encoding=encode))
    print('Loaded kbDict completely! kbDic length is '+ str(len(kbDict)))
    qtList = loadQtList(pathQt, encode)
    print('Loaded qtList completely! qtList length is '+ str(len(qtList)))
    countCharDict = loadcountCharDict(pathCD)
    print('Loaded countCharDict completely! countCharDict length is '+ str(len(countCharDict)))
    stemmingDict = json.load(open(pathSD, 'r',encoding='utf8'))
    print('Loaded stemmingDict completely! stemmingDict length is '+ str(len(stemmingDict)))
    vectorDict = loadvectorDict(pathVD)
    print('Loaded vectorDict completely! vectorDict length is '+ str(len(vectorDict)))
    answerAllQ(pathInput, pathOutput, n2eDict, kbDict, qtList, countCharDict, stemmingDict, vectorDict, qIDstart=1,wP=wP)


def tuningWeight(pathInput, pathOutput, n2eDict, kbDict, qtList, countCharDict, stemmingDict, vectorDict, entityCountDict ={},qIDstart=1, wP=10, wAP = 1):
    weightTuned = []
    maxAccuracy = 0
    for i in range(100):
        for j in range(100):
            accuracy = answerAllQ(pathInput, pathOutput, n2eDict, kbDict, qtList, countCharDict, \
                                  stemmingDict, vectorDict, entityCountDict = entityCountDict,qIDstart=1, wP=i+1, wAP = j+1)
            if maxAccuracy < accuracy:
                maxAccuracy = accuracy
            weightTuned.append([i+1,j+1,accuracy])
    
    print('maxAccuracy : ',maxAccuracy)
    fo = open('tuningWeight.txt','w',encoding='utf8')
    fo.write('maxAccuracy: '+str(maxAccuracy) + '\n')
    for l in weightTuned:
        fo.write(l+'\n')
    fo.close()
        
            

if len(sys.argv) == 11:
    pathInput=sys.argv[1]
    pathOutput=sys.argv[2]
    pathn2eDict=sys.argv[3]
    pathDict=sys.argv[4]
    pathQt=sys.argv[5]
    pathCD=sys.argv[6]
    pathSD=sys.argv[7]
    pathVD=sys.argv[8]
    qIDstart=int(sys.argv[9])
    defaultWeightPre=float(sys.argv[10])
    loadResAndanswerAllQ(pathInput, pathOutput, pathn2eDict, pathDict, pathQt, pathCD, pathSD, pathVD, 'utf8', qIDstart, defaultWeightPre)
