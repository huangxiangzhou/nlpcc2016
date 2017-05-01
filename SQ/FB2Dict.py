import json


fi = open('freebase-FB2M.txt.RD.RP','r',encoding='utf8')


d = {}

count = 0
for line in fi:
    if line == '':
        continue
    lineTmp = line.strip().lower().replace('/','.')
    tabIndex = lineTmp.index('\t')
    subject = lineTmp[:tabIndex]
    lineTmp = lineTmp[tabIndex + 1:]
    tabIndex = lineTmp.index('\t')
    predicate = lineTmp[:tabIndex].replace('_',' ')
    lineTmp = lineTmp[tabIndex + 1:]
    if subject not in d:
        d[subject] = {}
    if predicate not in d[subject]:
        d[subject][predicate] = set()
    for obj in lineTmp.split(' '):
        d[subject][predicate].add(obj)

    count += 1
    if count % 10000 == 0:
        print(str(count),end='\r',flush=True)

print('\n'+str(len(d)))

for key in d:
    for pre in d[key]:
        d[key][pre] = list(d[key][pre])



json.dump(d,open('FB2M.json','w',encoding='utf8'))
