import codecs
import sys
import re


def getCoreQuestion(inputPath='testing-data', outputPath='testing-data-core'\
                  ,encode = 'utf8'):

    p1 = re.compile(r'(啊|呀|(你知道)?吗|呢)?(？|\?)*$')
    p2 = re.compile(r'来着')
    p3 = re.compile(r'^呃(······)?')
    p4 = re.compile(r'^请问(一下|你知道)?')
    p5 = re.compile(r'^(那么|什么是|我想知道|我很好奇|有谁了解|问一下|请问你知道|谁能告诉我一下)')
    p6 = re.compile(r'^((谁|(请|麻烦)?你|请|)?(能|告诉)?告诉我)')
    p7 = re.compile(r'^((我想(问|请教)一下)，?)')
    p8 = re.compile(r'^((有人|谁|你|你们|有谁|大家)(记得|知道))')

    lPatten = [p1,p2,p3,p4,p5,p6,p7,p8]
    
    fi = open(inputPath,'r',encoding=encode)
    fo = open(outputPath,'w',encoding=encode)
    lineTmp = ''
    i = 0
    for line in fi:
        lineTmp = line.strip()
        for patten in lPatten:
            lineTmp, num = patten.subn('', lineTmp)
        fo.write(lineTmp+'\n')
        i += 1
        print('Processed ' + str(i) + ' \tQ.', end='\r', flush=True)

    fi.close()
    fo.close()

print('\nAll Done!')
getCoreQuestion()

input()
