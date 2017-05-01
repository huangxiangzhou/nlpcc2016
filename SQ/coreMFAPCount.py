import sys
import codecs
import lcs   #the lcs module is in extension folder
import time
import json
import re
import Levenshtein



class answerCandidate:
    def __init__(self, sub = ['',''], pre = '', qRaw = '', score = 0, kbDict = [], wS = 1, wP = 10, wAP = 10):
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
        self.scoreSubC = 0  
        self.scorePreLast = 0
        self.scorePreAll = 0
        self.scorePre = 0
        self.scoreAP = 0
        self.scoreAPAv = 0
        self.scoreAPS = 0
        self.scoreAPSAv = 0
        self.scoreList = []
        self.qt = []
        self.preCount = 0
        self.entityCount = []
   


    def calScoreSub(self, countCharDict):

        distance = Levenshtein.ratio
        q = self.qRaw
        scoreSub = 0

        sub = ''
        
        if type(self.sub) == str:
            
            sub = self.sub
            subSplit = sub.split(' ')
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
        
        return scoreSub


    def calScoreSubC(self):

        q = self.qRaw
        scoreSubC = 0

        if type(self.sub) == str:            
            sub = self.sub            
            if sub in q:
                scoreSubC = len(sub)
            else:
                subSplit = sub.split(' ')
                subSet = set(subSplit)
                qSet = set(q.split(' '))
                for w in (subSet & qSet):
                    scoreSubC += len(w)
                

        if type(self.sub) == list:
            for s in self.sub[0]:
                sub += s + ' '
            scoreSubC = len(sub)

        self.scoreSubC = scoreSubC
                
        return scoreSubC

    def calScorePreLast(self, countCharDict,qWithoutSubSet,stemmingDict):

        distance = Levenshtein.ratio
        pre = self.pre
        scorePre = 0

        lastPreIndex = pre.rfind('.')
        if lastPreIndex != -1:
            preLowerSet = set(re.split(r' ',pre[lastPreIndex+1:]))
        else:
            preLowerSet = set(re.split(r' ',pre))

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



        self.scorePreLast = scorePre

        
        return scorePre


    def calScorePreAll(self, countCharDict, qWithoutSubSet,stemmingDict):

        distance = Levenshtein.ratio
        pre = self.pre
        scorePre = 0

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



        self.scorePreAll = scorePre

        
        return scorePre

        

    def calcScore(self, qtList, countCharDict, debug=False, includingObj = [], vectorDict = {}, stemmingDict = {}, matchQt = False):

        scoreSub = self.calScoreSub(countCharDict)
        scoreSubC = self.calScoreSubC()
        

        q = self.qRaw         
        sub = ''
        if type(self.sub) == str:            
            sub = self.sub                

        if type(self.sub) == list:
            for s in self.sub[0]:
                sub += s + ' '
            sub = sub.strip()


        qWithoutSub = q.replace(sub,'').replace('  ', ' ').strip()

        qWithoutSubSet = set(qWithoutSub.split(' '))

        qWithoutSub = list(qWithoutSubSet)
        qWithoutSubSet = set()

        for i in range(len(qWithoutSub)):
            if qWithoutSub[i] in stemmingDict:
                qWithoutSub[i] = stemmingDict[qWithoutSub[i]][0][0]
            qWithoutSubSet.add(qWithoutSub[i])

        scorePreLast = self.calScorePreLast(countCharDict,qWithoutSubSet,stemmingDict)
        
        scorePreAll = self.calScorePreAll(countCharDict,qWithoutSubSet,stemmingDict)


        scoreAP = 0
        scoreAPAv = 0
        scoreAPS = 0
        scoreAPSAv = 0

    
        pre = self.pre
        qtKey = q.replace(sub,'(SUB)',1)
        distance = Levenshtein.ratio
        if pre in qtList:
            if qtKey in qtList[pre]:
                qtCount = qtList[pre][qtKey]
                scoreAP = qtCount 
                scoreAPAv = qtCount
                scoreAPS = qtCount
                scoreAPSAv = qtCount
            else:
                scoreMatch = 0
                scoreMatchSum = 0
                scoreSetMatch = 0
                scoreSetMatchSum = 0
                for qt in qtList[pre]:
                    scoreMatch = distance(qt, qtKey)
                    scoreMatchSum += scoreMatch
                    qtSet = set(qt.split(' '))
                    qtKeySet = set(qtKey.split(' '))
                    scoreSetMatch = len(qtSet & qtKeySet)/(len(qtSet | qtKeySet))
                    scoreSetMatchSum += scoreSetMatch

                    if scoreMatch > scoreAP:
                        scoreAP = scoreMatch


                    if scoreSetMatch > scoreAPS:
                        scoreAPS = scoreSetMatch


                scoreAPAv = scoreMatchSum / len(qtList[pre])

                scoreAPSAv = scoreSetMatchSum / len(qtList[pre])

        else:
            scoreAP = 0
            scoreAPAv = 0
            scoreAPS = 0
            scoreAPSAv = 0
                    
        self.scoreAP = scoreAP

        self.scoreAPAv = scoreAPAv
        self.scoreAPS = scoreAPS
        self.scoreAPSAv = scoreAPSAv
             

        self.score = scoreSub * 1 + scoreSubC * 1 + scorePreLast * 3 + scorePreAll * 3 + scoreAP * 5 + scoreAPAv * 5 + scoreAPS * 5 + scoreAPSAv * 5

        self.scoreList = [scoreSub, scoreSubC, scorePreLast, scorePreAll, scoreAP, scoreAPAv, scoreAPS, scoreAPSAv]
        
        return self.score
     

def getAnswer(sub, pre, kbDict):
    answerList = []
    for kb in kbDict[sub]:
        if pre in kb:
            answerList.append(kb[pre])
   
    return answerList

    



def answerQ (qRaw, n2eDict, kbDict, qtList, countCharDict, stemmingDict, vectorDict, entityCountDict = {}, n2eDictExt = {},wP=10, wAP =1,threshold=0, debug=False, tuningWeight = False):
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
                nGramSet.add(strNGram.replace('\'','')) 
            if '\"' in strNGram:
                nGramSet.add(strNGram.replace('\"',''))
                    


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

##  self.score = scoreSub * 1.58686519 + scoreSubC *1 + scorePreLast * 1.04220295 + scorePreAll * 1.04220295 + scoreAP * 7.72073936 + scoreAPAv * 1 + scoreAPS * 1 + scoreAPSAv * 1
     

    candidateSample = []       
    bestScorePre = 0

    scoreMax = 0
    for aCandidate in candidateSet:
        scoreTmp = aCandidate.calcScore(qtList, countCharDict, debug, stemmingDict = stemmingDict,matchQt = False)
        if scoreTmp > scoreMax:
            scoreMax = scoreTmp
            bestAnswer = set()
            bestScorePre = 0
        if scoreTmp == scoreMax:
            if bestScorePre < aCandidate.scorePre:
                bestScorePre = aCandidate.scorePre                
            bestAnswer.add(aCandidate)

        if tuningWeight == True:
            candidateSample.append([[aCandidate.entity,aCandidate.pre],[aCandidate.scoreSub,aCandidate.scoreSubC,aCandidate.scorePreLast,aCandidate.scorePreAll,\
                                                                        aCandidate.scoreAP,aCandidate.scoreAPAv,aCandidate.scoreAPS,aCandidate.scoreAPSAv]])
                    

    if tuningWeight == True:              
        return candidateSample

    for answer in bestAnswer:
        answer.preCount = len(kbDict[answer.entity])
        if len(entityCountDict) != 0:
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

def answerAllQ(pathInput, pathOutput, n2eDict, kbDict, qtList, countCharDict, \
               stemmingDict, vectorDict, entityCountDict ={},n2eDictExt = {},qIDstart=1, wP=10, wAP = 10):
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

        result = answerQ(q, n2eDict, kbDict, qtList, countCharDict, stemmingDict, vectorDict,\
                         entityCountDict =entityCountDict,n2eDictExt = n2eDictExt,wP=wP,wAP =wAP)

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
                         + str(res.scoreList) + '\n'

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
            if res.sub != goldenSub and res.scoreAP <= 1:
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
            goldenStr = goldenSP[i]+ '\t'+str(goldenAnswerSelected.scoreList) +'\n'
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


def tuningWeight(pathInput, pathOutput, n2eDict, kbDict, qtList, countCharDict, stemmingDict, vectorDict, entityCountDict ={},n2eDictExt = {}, qIDstart=1, wP=10, wAP = 10):

    fi = open(pathInput,'r',encoding='utf8')
    fo = open(pathOutput,'w',encoding='utf8')
    fo.close()
    maxLenC = 0
    count = 0
    maxLenCF = 0
    start = time.time()
    for line in fi:
        if line.strip() == '':
            continue
        lSplited = line.strip().split('\t')
        candidateSample = answerQ (lSplited[2], n2eDict, kbDict, qtList, countCharDict, stemmingDict, vectorDict, entityCountDict = entityCountDict, n2eDictExt = n2eDictExt,wP=wP, wAP =wAP,threshold=0, debug=False, tuningWeight = True)
        lenC = len(candidateSample)
        if maxLenC < lenC:
           maxLenC = lenC
        index = -1
        for i in range(lenC):
            if candidateSample[i][0][0] == lSplited[0] and candidateSample[i][0][1] == lSplited[1]:
                index = i

        if index == -1:
            continue

        candidateSampleFiltered = [candidateSample[index]]
        for i in range(len(candidateSample)):
            if i == index:
                continue
            foundBetter = False
            for j in range(len(candidateSample)):
                if i == j:
                    continue
                foundBetter = True
                for k in range(len(candidateSample[j][1])):
                    if candidateSample[j][1][k] <= candidateSample[i][1][k]:
                        foundBetter = False
                        break
                if foundBetter == True:
                    break

            if foundBetter == False:
                candidateSampleFiltered.append(candidateSample[i])
                
        lenCF = len(candidateSampleFiltered)
        
        if maxLenCF < lenCF:
           maxLenCF = lenCF
        fo = open(pathOutput,'a',encoding='utf8')
        fo.write(str([0, lenCF]) + '\t')
        for c in candidateSampleFiltered:
            fo.write(str(c[1]) + '\t')
        fo.write('\n')
        fo.close()
        count += 1
        print(count,'\t',str((time.time()-start)/count)[:6]+'\t',maxLenCF,maxLenC,end='\r',flush=True)
    
    
    
    
        
            

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

else:
    pathInput = 'valid-data'
    pathOutput = 'candidateScore'
    n2eDict = json.load(open('n2eDict','r',encoding='utf8'))
    kbDict = json.load(open('kbDict','r',encoding='utf8'))
    qtList = json.load(open('qtList','r',encoding='utf8'))
    countCharDict = json.load(open('countCharDict','r',encoding='utf8'))
    stemmingDict = json.load(open('stemmingDict','r',encoding='utf8'))
    vectorDict = json.load(open('vectorDict','r',encoding='utf8'))
    entityCountDict = json.load(open('entityCountDict','r',encoding='utf8'))
    
    tuningWeight(pathInput, pathOutput, n2eDict, kbDict, qtList, countCharDict, stemmingDict, vectorDict, entityCountDict = entityCountDict,n2eDictExt = {}, qIDstart=1, wP=10, wAP = 10)

