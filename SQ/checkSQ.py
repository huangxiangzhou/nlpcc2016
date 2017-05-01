



fb = open('freebase-FB2M.txt.RD','r',encoding='utf8')

fbSet = set()

for line in fb:
    tabIndex = line.replace('\t','S',1).find('\t')
    fbSet.add(line[:tabIndex])


count = [0,0,0,len(fbSet)]

for line in open('annotated_fb_data_test.txt','r',encoding='utf8'):
    tabIndex = line.replace('\t','S',1).find('\t')
    if line[:tabIndex] not in fbSet:
        print(line)
        count[0] += 1

for line in open('annotated_fb_data_train.txt','r',encoding='utf8'):
    tabIndex = line.replace('\t','S',1).find('\t')
    if line[:tabIndex] not in fbSet:
        print(line)
        count[1] += 1

for line in open('annotated_fb_data_valid.txt','r',encoding='utf8'):
    tabIndex = line.replace('\t','S',1).find('\t')
    if line[:tabIndex] not in fbSet:
        print(line)
        count[2] += 1

print(str(count))




    
