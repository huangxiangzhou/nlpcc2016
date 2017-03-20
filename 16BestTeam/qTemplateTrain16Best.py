import sys
import codecs
import json
import re



inputEncoding = 'utf8'
outputEncoding = 'utf16'

fi = open(sys.argv[1], 'r', encoding=inputEncoding)
fo = open(sys.argv[2], 'w', encoding=outputEncoding)

qRaw = ''
p1 = re.compile(r'(啊|呀|(你知道)?吗|呢)?(？|\?)*$')
p2 = re.compile(r'来着')
p3 = re.compile(r'^呃(······)?')
p4 = re.compile(r'^请问(一下|你知道)?')
p5 = re.compile(r'^(那么|什么是|我想知道|我很好奇|有谁了解|问一下|请问你知道|谁能告诉我一下)')
p6 = re.compile(r'^((谁|(请|麻烦)?你|请|)?(能|告诉)?告诉我)')
p7 = re.compile(r'^((我想(问|请教)一下)，?)')
p8 = re.compile(r'^((有人|谁|你|你们|有谁|大家)(记得|知道))')

lPatten = [p1,p2,p3,p4,p5,p6,p7,p8]


APList = {}
for line in fi:
    if line.find('<q') == 0:  #question line
        qRaw = line[line.index('>') + 2:].strip().lower().replace(' ', '')
        for patten in lPatten:
            qRaw, num = patten.subn('', qRaw)
        continue
    elif line.find('<t') == 0:  #triple line
        triple = line[line.index('>') + 2:]
        s = triple[:triple.index(' |||')].strip().lower().replace(' ', '')
        triNS = triple[triple.index(' |||') + 5:]
        p = triNS[:triNS.index(' |||')].strip().lower().replace('-', '').replace('路', '').replace(' ', '')
        if qRaw.find(s) != -1:
            qRaw = qRaw.replace(s,'(SUB)', 1)
       
        qRaw = qRaw.strip() +  ' ||| '  + p
        if qRaw in APList:
            APList[qRaw] += 1
        else:
            APList[qRaw] = 1
    else: continue

json.dump(APList, fo)

fo2 = open(sys.argv[2]+'.txt', 'w', encoding=outputEncoding)

for line in APList:
    fo2.write(line+'\n')
    
fo2.close() 


fi.close()    
fo.close()    
