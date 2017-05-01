

fa = open('annotated_fb_data_test.nq.map','r',encoding='utf8')

laPre = []
for line in fa:
    lineTmp = line.strip()
    if lineTmp == '':
        print('fa!!!')
        continue
    tabIndex = lineTmp.replace('\t','S',1).find('\t')
    laPre.append(lineTmp[:tabIndex])

fa2 = open('answer','r',encoding='utf8')

laPre2 = []


for line in fa2:
    lineTmp = line.strip()
    if lineTmp == '':
        print('fa2!!!')
        continue
    lineTmp = lineTmp.split('\t|||\t')
    lRs = []
    for lStr in lineTmp:
        tabIndex = lStr.replace('\t','S',1).find('\t')
        if tabIndex != -1:
            lRs.append(lStr[:tabIndex])
    laPre2.append(lRs)


count1 = 0
countN = 0

print(len(laPre),len(laPre2))


for i in range(len(laPre)):
    for lStr in laPre2[i]:
        if lStr == laPre[i]:
            countN += 1
            if len(laPre2[i]) == 1:
                count1 += 1
            continue
    
    
    


Accuracy1 = count1 / len(laPre)
AccuracyN = countN / len(laPre)


print('Accuracy@1:\t',Accuracy1)
print('Accuracy@Infinite:\t',AccuracyN)



        
