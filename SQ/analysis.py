import json
import lcs




#e2nDict = json.load(open('../entity2name.lowcase.json','r',encoding='utf8'))

def compareAnswer(e2nDict):
    fq = open('annotated_fb_data_test.question','r',encoding='utf8')

    fta = open('annotated_fb_data_test.sp.map','r',encoding='utf8')

    fa = open('answer','r',encoding='utf8')

    fo = open('answerCompareND.txt','w',encoding='utf8')

    lq = []
    lta = []
    la = []


    for line in fq:
        lq.append(line.strip())

    for line in fta:
        lta.append(line.strip())


    for line in fa:
        la.append(line.strip())


    for i in range(min(len(lq),len(lta),len(la))):
        if la[i].find('|||') == -1:
            tabIndexScore = la[i].replace('\t','S',1).find('\t')
            if tabIndexScore != -1:
                laiTmp = la[i][:tabIndexScore]
            else:
                laiTmp = la[i]
            if lta[i] != laiTmp:
                tabIndex = lta[i].find('\t')
                subject1 = lta[i][:tabIndex]
                predicate1 = lta[i][tabIndex + 1:]

                if subject1 in e2nDict:
                    subject1 = str(e2nDict[subject1])

                tabIndex = laiTmp.find('\t')
                
                subject2 = laiTmp[:tabIndex]
                predicate2 = laiTmp[tabIndex + 1:]

                if subject2 in e2nDict:
                    subject2 = str(e2nDict[subject2])

                if subject1 == subject2 and predicate1 == predicate2:               
                    fo.write('Question(S1P1==S2P2):\t' + lq[i] + '\n')
                else:
                    fo.write('Question:\t' + lq[i] + '\n')
                fo.write('Right:\t' + subject1 + '\t' + predicate1 + '\n')
                fo.write('Wrong:\t' + subject2 + '\t' + predicate2 + '\n')




def formatQuestionSet(e2nDict):
    fq = open('annotated_fb_data_test.txt.map','r',encoding='utf8')
    fo = open('testdata','w',encoding='utf8')
    for line in fq:
        lineTmp = line.replace('www.freebase.com/','').strip()
        tabIndex = lineTmp.index('\t')
        subject = lineTmp[:tabIndex].replace('/','.')
        subjectSet = []
        fo.write(subject + ' : ')

        if subject in e2nDict:
            subjectSet = e2nDict[subject]

        fo.write(str(subjectSet) + ' ||| ')
        lineTmp = lineTmp[tabIndex + 1:]
        tabIndex = lineTmp.index('\t')
        predicate = lineTmp[:tabIndex].replace('/','.')
        fo.write(predicate + '\tQ: ')
        lineTmp = lineTmp[tabIndex + 1:]
        tabIndex = lineTmp.index('\t')
        q = lineTmp[tabIndex + 1:]
        fo.write(q+'\n')





























    
            
