import json


def repalceDataset():
    fi = open('annotated_fb_data_test.txt','r',encoding='utf8')


    keyMappingDict = json.load(open('keyReplaceBy.json','r',encoding='utf8'))
    fo = open('test-data','w',encoding='utf8')


    for line in fi:
        if line.strip() == '':
            continue
        lineTmp = line.replace('www.freebase.com/','').strip()
        qTabIndex = lineTmp.replace('\t','T',2).find('\t')
        q = lineTmp[qTabIndex + 1:]
        
        tabIndex = lineTmp.index('\t')
        subject = lineTmp[:tabIndex].replace('/','.')
        if subject in keyMappingDict:
            subject = keyMappingDict[subject]

        preTabIndex = lineTmp.replace('\t','T',1).find('\t')
        pre = lineTmp[tabIndex+1:preTabIndex].replace('/','.').replace('_',' ')


        fo.write(subject+'\t'+pre+'\t'+q+'\n')


    fi.close()
    fo.close()


repalceDataset()
##
##keyMappingDict = json.load(open('keyReplaceBy.json','r',encoding='utf8'))
##FBDict = json.load(open('FB2M.json','r',encoding='utf8'))
##
##
##for key in list(FBDict):
##    if key in keyMappingDict:
##        FBDict[keyMappingDict[key]] = FBDict[key]                    
##        del FBDict[key]
##
##
##for key in list(FBDict):
##    for pre in FBDict[key]:
##        for i in range(len(FBDict[key][pre])):
##            if FBDict[key][pre][i] in keyMappingDict:
##                FBDict[key][pre][i] = keyMappingDict[FBDict[key][pre][i]]
##
##json.dump(FBDict,open('FB2M.map.json','w',encoding='utf8'))
