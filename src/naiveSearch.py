import sys
import codecs
import lcs
import Levenshtein
import time

class answerCandidate:
    def __init__(self, sub = '', pre = '', qRaw = '', qType = 0, score = 0, kbDict = []):
        self.sub = sub     
        self.pre = pre     
        self.qRaw = qRaw     
        self.qType = qType
        self.score = score
        self.kbDict = kbDict

    def calcScore(self, qtList):
        lcsSub = lcs.lcs(self.sub, self.qRaw)
        subIndex = self.qRaw.index(lcsSub)
        qTemplate = self.qRaw.replace(lcsSub, '')
        if self.pre == '':
            self.qType = 2
        else:
            lcsPre = lcs.lcs(self.pre, qTemplate)
            preIndex = qTemplate.index(lcsPre)
            qTemplate = qTemplate.replace(lcsPre, '')
            if preIndex < subIndex:
                self.qType = 1
        
        if self.qType == 0:
            qt01 = qTemplate[:subIndex]
            qt02 = qTemplate[subIndex:preIndex]
            qt03 = qTemplate[preIndex:]
            mSqt01 = 0
            mSqt02 = 0
            mSqt03 = 0
            for vQt01 in qtList['01']:
                tmp = Levenshtein.jaro(qt01,vQt01)
                if tmp > mSqt01:
                    mSqt01 = tmp
            for vQt02 in qtList['02']:
                tmp = Levenshtein.jaro(qt02,vQt02)
                if tmp > mSqt02:
                    mSqt02 = tmp
            for vQt03 in qtList['03']:
                tmp = Levenshtein.jaro(qt03,vQt03)
                if tmp > mSqt03:
                    mSqt03 = tmp
            self.score = (mSqt01 + mSqt02 + mSqt03 + Levenshtein.jaro(lcsSub, self.sub) + Levenshtein.jaro(lcsPre, self.pre))/5
        if self.qType == 1:
            qt11 = qTemplate[:preIndex]
            qt12 = qTemplate[preIndex:subIndex]
            qt13 = qTemplate[subIndex:]
            mSqt11 = 0
            mSqt12 = 0
            mSqt13 = 0
            for vQt11 in qtList['11']:
                tmp = Levenshtein.jaro(qt11,vQt11)
                if tmp > mSqt11:
                    mSqt11 = tmp
            for vQt12 in qtList['12']:
                tmp = Levenshtein.jaro(qt12,vQt12)
                if tmp > mSqt12:
                    mSqt12 = tmp
            for vQt13 in qtList['13']:
                tmp = Levenshtein.jaro(qt13,vQt13)
                if tmp > mSqt13:
                    mSqt13 = tmp
            self.score = (mSqt11 + mSqt12 + mSqt13 + Levenshtein.jaro(lcsSub, self.sub) + Levenshtein.jaro(lcsPre, self.pre))/5


        if self.qType == 2:
            qt20 = qTemplate
            qt21 = qTemplate[:subIndex]
            qt22 = qTemplate[subIndex:]
            mSqt20 = 0
            preResult = set()
            for vQt20 in qtList['20']:
                vQt201 = vQt20[:vQt20.index('|||qS|||')]
                vQt202 = vQt20[vQt20.index('|||qS|||') + 8:vQt20.index(' ===>>> ')]
                vQt20pre = vQt20[vQt20.index(' ===>>> ') + 8:]
                sTmp20 = Levenshtein.jaro(vQt201,qt21) + Levenshtein.jaro(vQt202,qt22)
                sTmp20pre = 0
                preTmp = set()
                for kb in self.kbDict:
                    for pre in kb:
                        tmp = Levenshtein.jaro(vQt20pre,pre)
                        if tmp > sTmp20pre :
                            sTmp20pre = tmp
                            preTmp = set()
                        if tmp == sTmp20pre :
                            preTmp.add(pre)
                sTmp20 = (sTmp20 + sTmp20pre + Levenshtein.jaro(lcsSub, self.sub))/4
                if sTmp20 > mSqt20:
                    mSqt20 = sTmp20
                    preResult = set()
                if sTmp20 == mSqt20:
                    for pre in preTmp:
                        preResult.add(pre)
            self.pre = preResult
            self.score = mSqt20
        return self.score

def getAnswer(sub, pre, kbDict):
    for kb in kbDict[sub]:
        if pre in kb:
            return kb[pre]
    return 'NO ANSWER FOUND BY QA SYSTM'



def answerAllQ(pathInput, pathOutput, lKey, kbDict, qtList):
    fq = open(pathInput, 'r', encoding='utf8')
    i = 0
    timeStart = time.time()
    for line in fq:
        i += 1
        fo = open(pathOutput, 'a', encoding='utf8')
        q = str(line.strip())
        result = answerQ(q, lKey, kbDict, qtList)
        fo.write('<question id='+str(i)+'>\t' + q + '\n')
        if len(result) != 0:
            answerSet = set()
            fo.write('<triple id='+str(i)+'>\t')
            for res in result:
                if res.qType == 2:
                    for pre in res.pre:
                        answerTmp = getAnswer(res.sub, pre, kbDict)
                        answerSet.add(answerTmp)
                        fo.write(res.sub + ' ||| ' + pre + ' ||| ' + answerTmp + ' ====== ')
                else:
                    answerTmp = getAnswer(res.sub, res.pre, kbDict)
                    answerSet.add(answerTmp)
                    fo.write(res.sub + ' ||| ' + res.pre + ' ||| ' + answerTmp + ' ====== ')
            fo.write('\n')
            fo.write('<answer id='+str(i)+'>\t')
            for ansTmp in answerSet:
                fo.write(ansTmp)
                if len(answerSet) > 1:
                    fo.write(' ||| ')
            fo.write('\n==================================================\n')
            
        print('processing ' + str(i) + 'th Q, average time cost: ' + str((time.time()-timeStart) / i) + 'Second', end = '\r', flush=True)
        fo.close()
    fq.close()
    



def answerQ (qRaw, lKey, kbDict, qtList, threshold=0):
    q = qRaw.strip().replace(' ','')
    qtType = 0 #0:sub+pre 1:pre+sub 2:sub

    maxSubLen = 0
    maxSubSetTmp = set()
    maxSubSet = set()
    maxPreLen = 0
    maxPreSet = set()
    maxSPLen = 0
    maxSPSet = set()
    
    result = ''
    lcsSub = ''
    lcstemp = ''
    lcsPre = ''
    subIndex = 0
    scoreSub = 0
    qRemoveSub = ''
    
    preIndex = 0
    scoreSub = 0
    qRemoveSubPre = ''

    maxScore = 0

    for key in lKey:
        lcsSub = lcs.lcs(q,key)
        if lcsSub == '':
            continue
        lcsSubLen = len(lcsSub)
        if maxSubLen < lcsSubLen:
            maxSubSetTmp = set()
            maxSubLen = lcsSubLen

        if maxSubLen == lcsSubLen:                      
            maxSubSetTmp.add(key)
            
    
    for key in lKey:
        lcsSub = lcs.lcs(q,key)
        if lcsSub == '':
            continue
        lcsSubLen = len(lcsSub)
      
        lcsSubIndex = q.index(lcsSub)
        qRemoveSub1 = q[:lcsSubIndex]
        qRemoveSub1Len = len(qRemoveSub1)
        qRemoveSub2 = q[lcsSubIndex + lcsSubLen:]
        qRemoveSub2Len = len(qRemoveSub2)
        for kb in kbDict[key]:    
            for pre in list(kb) :
                preLen = len(pre)
                if maxSubLen == lcsSubLen : 
                    if qRemoveSub1Len > maxPreLen:
                        lcsPre1 = lcs.lcs(qRemoveSub1, pre)
                    if qRemoveSub2Len > maxPreLen:
                        lcsPre2 = lcs.lcs(qRemoveSub2, pre)
                    if lcsPre1 != '' or lcsPre2 != '':
                        newAnswerCandidate = answerCandidate(key, pre, q)
                    else:
                        newAnswerCandidate = answerCandidate(key, '', q, 2, 0, kbDict[key])
                    maxSubSet.add(newAnswerCandidate)
                    
                if preLen > maxPreLen:
                    if qRemoveSub1Len > maxPreLen:
                        lcsPre1 = lcs.lcs(qRemoveSub1, pre)
                    if qRemoveSub2Len > maxPreLen:
                        lcsPre2 = lcs.lcs(qRemoveSub2, pre)
                    maxLcsPre12 = max(len(lcsPre1),len(lcsPre2))
                    if maxLcsPre12 > maxPreLen :
                        maxPreLen = maxLcsPre12
                        maxPreSet = set()
                    if maxLcsPre12 == maxPreLen :
                        newAnswerCandidate = answerCandidate(key, pre, q)
                        maxPreSet.add(newAnswerCandidate)

                maxResidual = maxSPLen - lcsSubLen
                if preLen > maxResidual :
                    if qRemoveSub1Len > maxResidual:
                        lcsPre1 = lcs.lcs(qRemoveSub1, pre)
                    if qRemoveSub2Len > maxResidual:
                        lcsPre2 = lcs.lcs(qRemoveSub2, pre)
                    maxResidual12 = max(len(lcsPre1),len(lcsPre2))
                    if maxResidual12 > maxResidual :
                        maxSPLen = maxResidual12 + lcsSubLen
                        maxResidual = maxSPLen - lcsSubLen
                        maxSPSet = set()
                    if maxResidual12 == maxResidual :
                        newAnswerCandidate = answerCandidate(key, pre, q)
                        maxSPSet.add(newAnswerCandidate)

    bestAnswer = set()
    
    maxSubSetCopy = maxSubSet.copy()
    maxSubSet = set()
    for aCandidate in maxSubSetCopy:
        aCfound = 0
        for aC in maxSubSet:
            if aC.pre == aCandidate.pre and aC.sub == aCandidate.sub:
                aCfound = 1
                break
        if aCfound == 0:
            maxSubSet.add(aCandidate)

    maxPreSetCopy = maxPreSet.copy()
    maxPreSet = set()
    for aCandidate in maxPreSetCopy:
        aCfound = 0
        for aC in maxPreSet:
            if aC.pre == aCandidate.pre and aC.sub == aCandidate.sub:
                aCfound = 1
                break
        if aCfound == 0:
            maxPreSet.add(aCandidate)

    maxSPSetCopy = maxSPSet.copy()
    maxSPSet = set()
    for aCandidate in maxSPSetCopy:
        aCfound = 0
        for aC in maxSPSet:
            if aC.pre == aCandidate.pre and aC.sub == aCandidate.sub:
                aCfound = 1
                break
        if aCfound == 0:
            maxSPSet.add(aCandidate)

    for aCandidate in maxSubSet:
        scoreTmp = aCandidate.calcScore(qtList)
        if scoreTmp > maxScore:
            maxScore = scoreTmp
            bestAnswer = set()
        if scoreTmp == maxScore:
            bestAnswer.add(aCandidate)
            
    for aCandidate in maxPreSet:
        scoreTmp = aCandidate.calcScore(qtList)
        if scoreTmp > maxScore:
            maxScore = scoreTmp
            bestAnswer = set()
        if scoreTmp == maxScore:
            bestAnswer.add(aCandidate)

    for aCandidate in maxSPSet:
        scoreTmp = aCandidate.calcScore(qtList)
        if scoreTmp > maxScore:
            maxScore = scoreTmp
            bestAnswer = set()
        if scoreTmp == maxScore:
            bestAnswer.add(aCandidate)
            
    bestAnswerCopy = bestAnswer.copy()
    bestAnswer = set()
    for aCandidate in bestAnswerCopy:
        aCfound = 0
        for aC in bestAnswer:
            if aC.pre == aCandidate.pre and aC.sub == aCandidate.sub:
                aCfound = 1
                break
        if aCfound == 0:
            bestAnswer.add(aCandidate)
                        
    return bestAnswer #[bestAnswer,maxSubSet,maxPreSet,maxSPSet]


def loadQtList(path, encode = 'utf16'):
    qtList = {}
    qtList['01'] = set()
    qtList['02'] = set()
    qtList['03'] = set()
    qtList['11'] = set()
    qtList['12'] = set()
    qtList['13'] = set()
    qtList['20'] = set()
    qtList['21'] = set()
    qtList['22'] = set()
    for line in open(path + '01', 'r', encoding = encode):
        qtList['01'].add(line.strip())
    for line in open(path + '02', 'r', encoding = encode):
        qtList['02'].add(line.strip())
    for line in open(path + '03', 'r', encoding = encode):
        qtList['03'].add(line.strip())
    for line in open(path + '11', 'r', encoding = encode):
        qtList['11'].add(line.strip())
    for line in open(path + '12', 'r', encoding = encode):
        qtList['12'].add(line.strip())
    for line in open(path + '13', 'r', encoding = encode):
        qtList['13'].add(line.strip())
    for line in open(path + '20', 'r', encoding = encode):
        qtList['20'].add(line.strip())
    for line in open(path + '21', 'r', encoding = encode):
        qtList['21'].add(line.strip())
    for line in open(path + '22', 'r', encoding = encode):
        qtList['22'].add(line.strip())

    return qtList
        
        
    

                    
def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s1)):
        for y in range(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
                else:
                    m[x][y] = 0
    return s1[x_longest - longest: x_longest]
