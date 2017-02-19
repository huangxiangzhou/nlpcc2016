import sys
import codecs

fi = open(sys.argv[1], 'r', encoding='utf8')
j = 1
for line in fi:
    fo = open(sys.argv[2] + str(j), 'w', encoding='utf8')
    fo.write(line)
    for i in range(int(sys.argv[3]) - 1):        
        fo.write(fi.readline())
    fo.close()
    j = j + 1
fi.close()
    

    
