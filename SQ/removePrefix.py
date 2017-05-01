import sys
import codecs



fi = open('freebase-FB2M.txt.RD','r',encoding='utf8')

fo= open('freebase-FB2M.txt.RD.RP','w',encoding='utf8')

tmpLine = set()


for line in fi:
    fo.write(line.replace('www.freebase.com/',''))


fi.close()
fo.close()
