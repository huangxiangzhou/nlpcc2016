import json

def SimplifyN2EDict(dictToSimplify, pathEntityList = 'entityList.FB2M.json', pathOutput = 'name2entity.rp.lowcase.FB2M.json'):
    sDict = dictToSimplify.copy()

    entitySet = set(json.load(open(pathEntityList,'r',encoding='utf8')))
    count = 0
    print(len(sDict))
    for labels in dictToSimplify:       
        sDict[labels] = set(sDict[labels])
        for label in dictToSimplify[labels]:      
            if label not in entitySet:
                sDict[labels].remove(label)
        if len(sDict[labels]) == 0:
            del sDict[labels]
        else:
            sDict[labels] = list(sDict[labels])

        count += 1
        print(count,end='\r',flush=True)


    print('\n',len(sDict))
    json.dump(sDict,open(pathOutput,'w',encoding='utf8'))


def SimplifyE2NDict(dictToSimplify, pathEntityList = 'entityList.FB2M.json', pathOutput = 'entity2name.lowcase.FB2M.json'):
    sDict = dictToSimplify.copy()

    entitySet = set(json.load(open(pathEntityList,'r',encoding='utf8')))
    count = 0
    print(len(sDict))
    for entity in dictToSimplify:
        if entity not in entitySet:
            del sDict[entity]
        count += 1
        print(count,end='\r',flush=True)


    print('\n',len(sDict))
    json.dump(sDict,open(pathOutput,'w',encoding='utf8'))


def generateEntityList(kbDict, pathOutput = 'entityList.FB2M.json'):
    print(len(kbDict))
    count = 0
    entitySet = set()
    for key in kbDict:
        entitySet.add(key)
        for pre in kbDict[key]:
            for obj in kbDict[key][pre]:
                entitySet.add(obj)

    print('\n',len(entitySet))
    json.dump(list(entitySet),open(pathOutput,'w',encoding='utf8'))
