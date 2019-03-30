# -*- coding: utf-8 -*-
"""
Created on Mon Mar 4 14:05:33 2019

@author: fengbozheng
"""

#The Root of the hierarchy (or sub-hierarchy)
subhierarchyName = 'xxxxxxx'   #e.g."404684003"

#Step1 Preprocessing and make it ready for parsing
import string
allowed = string.letters + string.digits+ " " + "." + "-" + "/" +"'s"
def check_naive(mystring):
    return all(c in allowed for c in mystring)

digits = string.digits
def check_digits(string):
    return any(d in digits for d in string)

import networkx as nx
with open('HierarchicalRelation(ParentChild).txt') as f2:  
    lines= f2.readlines()
    Dirgraph2 = nx.read_edgelist(lines, create_using = nx.DiGraph(), nodetype = str)

def findSubHierarchy(node):
    Dic2 = dict(nx.bfs_successors(Dirgraph2,node))
    d2 = Dic2.values()
    c2 = []
    for e2 in d2:
        c2 = c2+e2
    return c2    

with open('HierarchicalRelation(ChildParent).txt') as f:  
    lines= f.readlines()
    Dirgraph = nx.read_edgelist(lines, create_using = nx.DiGraph(), nodetype = str)

def findAncestors(node):
    Dic = dict(nx.bfs_successors(Dirgraph,node))
    d = Dic.values()
    c = []
    for e in d:
        c = c+e
    return c     

nodesInHierarchy = set(findSubHierarchy(subhierarchyName))

file1 = open("FSN.txt","rb+") 
file2 = open("SplitFSN.txt","w")

for line in file1:
    if line.endswith(")\n"):
        lineL = line.split("(")
        lineWithoutSemanticTag = "(".join(lineL[0:(len(lineL)-1)])
        lineParen1 = lineWithoutSemanticTag.lower().replace("(","")
        lineParen2 = lineParen1.replace(")","")
        lineComa = lineParen2.replace(","," ")   
        lineAnd = lineComa.replace("&"," and ")    # will not be considered in the finding missing IS-A
        lineSP1 = lineAnd.replace("[","")
        lineSP2 = lineSP1.replace("]","")
        lineColumn = lineSP2.replace(":"," ")
        lineDash = lineColumn.replace(" - ", " ")
        lineDashD = lineDash.replace("--"," ")
        lineAdd = lineDash.replace("+"," and ")  # will not be considered in the finding missing IS-A
        lineSep = lineAdd.replace(';'," ")
        lineQuote = lineSep.replace('"','')
        lineQuoteS =lineQuote.replace("'","")
        line1 = lineQuoteS.split("\n")[0]
        line1List = line1.split("\t")
        conceptID = line1List[0]
        FSN = line1List[1]
        lexicalFeature = []
        if (conceptID in nodesInHierarchy):   
            lineList = FSN.split(" ")
            for item in lineList:
                if "/" in item:
                    if check_digits(item) == False:
                        tempList = item.split("/")
                        for i in range(0,(len(tempList)-1)):
                            lexicalFeature.append(tempList[i])
                            lexicalFeature.append("or")
                        lexicalFeature.append(tempList[len(tempList)-1])  # will not be considered in the finding missing IS-A
                    else:
                        lexicalFeature.append(item)
                else:
                    lexicalFeature.append(item)
            file2.write(conceptID+" "+" ".join(lexicalFeature)+"\n")
    else:
        lineParen1 = line.lower().replace("(","")
        lineParen2 = lineParen1.replace(")","")
        lineComa = lineParen2.replace(","," ")   
        lineAnd = lineComa.replace("&"," and ")    # will not be considered in the finding missing IS-A
        lineSP1 = lineAnd.replace("[","")
        lineSP2 = lineSP1.replace("]","")
        lineColumn = lineSP2.replace(":"," ")
        lineDash = lineColumn.replace(" - ", " ")
        lineDashD = lineDash.replace("--"," ")
        lineAdd = lineDashD.replace("+"," and ")  # will not be considered in the finding missing IS-A
        lineSep = lineAdd.replace(';'," ")
        lineQuote = lineSep.replace('"','')
        lineQuoteS =lineQuote.replace("'","")
        line1 = lineQuoteS.split("\n")[0]
        line1List = line1.split("\t")
        conceptID = line1List[0]
        FSN = line1List[1]
        lexicalFeature = []
        if (conceptID in nodesInHierarchy):   
            lineList = FSN.split(" ")
            for item in lineList:
                if "/" in item:
                    if check_digits(item) == False:
                        tempList = item.split("/")
                        for i in range(0,(len(tempList)-1)):
                            lexicalFeature.append(tempList[i])
                            lexicalFeature.append("or")
                        lexicalFeature.append(tempList[len(tempList)-1])  # will not be considered in the finding missing IS-A
                    else:
                        lexicalFeature.append(item)
                else:
                    lexicalFeature.append(item)
            file2.write(conceptID+" "+" ".join(lexicalFeature)+"\n")        

        
file1.close()
file2.close()
print "Preprocessing Finished"

# set up port and start server from terminal
'''
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
-preload tokenize,ssplit,pos,lemma,ner,parse,depparse \
-status_port 9000 -port 9000 -timeout 15000 & 
'''
#Step2 Parse the sentence
from nltk.parse import CoreNLPParser
parser = CoreNLPParser(url='http://localhost:9000')

file1 = open("SplitFSN.txt","rb+")
output1 = open("InitialLexicalFeatures.txt","w")

import string
allowed = string.letters + " "
def check_naive(mystring):     #just make sure the parser will combine words splitted by space only.
    return all(c in allowed for c in mystring)


for lines in file1:
    if check_naive(" ".join(lines.split()[1:len(lines.split())])):
        line = lines.split()
        conceptID = line[0]
        bagOfWordList = line[1:len(line)]
        b = parser.parse(bagOfWordList)
        s = str(list(b)).replace("[","").replace("]","").replace("Tree","").replace("'","")
        NPstart = False
        npList = []
        np = ""
        layer = 0
        for i in range(len(s)):
            if s[i] =="N" and s[i-1] == "(" and s[i+1] =="P" and s[i+2] ==",":
                if NPstart == False:
                    NPstart = True
                    layer = 1
                else:
                    np = ""
                    NPstart = True
                    layer = 1        
            if NPstart == True:
                if s[i] == "(":
                    layer = layer + 1
                if s[i] == ")":
                    layer = layer - 1
                if s[i] not in "()":
                    np = np + s[i]
                if layer == 0:
                    NPstart = False
                    npList.append(np)
                    np = ""
        nounPhraseList = []
        for np in npList:
            npp = []
            for item in np.split(", "):
                if item.isupper() == False:
                    npp.append(item) 
            nounPhraseList.append(" ".join(npp))
        #already got nounPhrases in nounPhraseList
        newList = []
        for i in range(len(nounPhraseList)):
            current = nounPhraseList[i]
            length = len(current.split(" "))
            findFlag = 0
            while findFlag ==0:    
                if " ".join(bagOfWordList[0:length]) == current:
                    newList.append(current)
                    del bagOfWordList[0:length]
                    findFlag = 1
                else:
                    newList.append(bagOfWordList[0])
                    del bagOfWordList[0]
        if len(bagOfWordList)>0:
            for restWord in bagOfWordList:
                newList.append(restWord)
        output1.write(conceptID+"&"+"&".join(newList)+"\n")
output1.close()
file1.close()
print "Noun Prase Identification Finished"


#Step3 Make subsuption test efficient and prepare for first-step enrichment
#Genrate All concepts and All lexical features:
fileFCA = open("AllFeatures.txt","w")
allattributes = set()
fileAllConceptInSub = open("AllConceptID.txt","w")
file2 = open("InitialLexicalFeatures.txt","rb+")

for lines in file2:
    line = lines.split("\n")[0]
    lineL = line.split("&")
    conceptID = lineL[0]
    lexicalL = lineL[1:len(lineL)]
    fileAllConceptInSub.write(conceptID+"\n")
    for eachOne in lexicalL:
        allattributes.add(eachOne)
        
for eachLexOne in allattributes:    
    fileFCA.write(eachLexOne)
    fileFCA.write("\n")
    
fileFCA.close()
fileAllConceptInSub.close()
file2.close()


#First step enrichment
conceptLex = {}
file3 = open("InitialLexicalFeatures.txt","rb+")
for lines in file3:
    line = lines.split("\n")[0]
    lineL = line.split("&")
    conceptID = lineL[0]
    lexicalL = lineL[1:len(lineL)]
    if conceptLex.get(conceptID,"default")=="default":
        conceptLex[conceptID] = lexicalL
    else:
        print "error"
file3.close()


fileAllConceptInSubOpen = open("AllConceptID.txt","rb+")
fileFCAOpen = open("AllFeatures.txt.txt","rb+")           
ConceptList = []
AttributeList = []

for eachConceptLine in fileAllConceptInSubOpen:
    eachConcept = eachConceptLine.split()[0]
    ConceptList.append(eachConcept)
fileAllConceptInSubOpen.close()

for eachAttributeLine in fileFCAOpen:
    Attribute = eachAttributeLine.split("\n")[0]
    AttributeList.append(Attribute)
fileFCAOpen.close()

file1Output = open("1stEnrichedLexicalFeatures.txt","w")

for iii in range(0,len(ConceptList)):
    #print iii
    file1Output.write(ConceptList[iii]+": ")
    lexF = conceptLex.get(ConceptList[iii])
    for jjj in range(0,len(AttributeList)):
        for everyAttributes in lexF:
            if (AttributeList[jjj] in everyAttributes) and (set(AttributeList[jjj].split(" ")).issubset(set(everyAttributes.split(" ")))):
                file1Output.write(str(jjj)+" ")
                break
    file1Output.write("\n")
file1Output.close()

#Compute Stop Concept: concepts contain stop word or antonym pair
file1 = open("StopWord.txt","rb+")
stopWord = set()
stopPhrase = set()
for line1 in file1:
    stopWordPhrase = line1.split()
    if len(stopWordPhrase) ==1:
        stopWord.add(stopWordPhrase[0])
    else:
        stopPhrase.add(" ".join(stopWordPhrase))

conceptWithStopWord = set()
file1= open("InitialLexicalFeatures.txt","rb+")
for lines in file1:
    line = lines.split("\n")[0]
    linee = line.split(" ")
    conceptID = linee[0] 
    conceptLexical= linee[1:len(linee)]
    if any(stopW in conceptLexical for stopW in stopWord) or any(((stopP in line) and (set(stopP.split()).issubset(set(conceptLexical)))) for stopP in stopPhrase):
        conceptWithStopWord.add(conceptID)

output2 = open("StopConcept.txt","w")
for everyConcept in conceptWithStopWord:
    output2.write(everyConcept+"\n")
output2.close()
file1.close()

#Second Step Enrichment
conceptWithStopWord = set()
file6 = open("StopConcept.txt","rb+")
for lines in file6:
    line = lines.split()
    conceptWithStopWord.add(line[0])
file6.close()

IDToLexical = {}
file1= open("1stEnrichedLexicalFeatures.txt","rb+")
for lines in file1:
    line = lines.split("\n")[0]
    linee = line.split(" ")
    conceptID = linee[0].split(":")[0] 
    conceptLexical= linee[1:len(linee)]
    if IDToLexical.get(conceptID,"default") == "default":
        IDToLexical[conceptID] = conceptLexical
    else:
        if conceptLexical !=IDToLexical.get(conceptID):
            print"error"+"multiple FSN for one ID"
            print conceptID
            print conceptLexical
            print IDToLexical.get(conceptID)
            continue
file1.close()

nodesConsidered = nodesInHierarchy.intersection(set(IDToLexical.keys())) - conceptWithStopWord       
        
output3 = open("2ndEnrichedLexicalFeatures.txt","w")
for eachConcepti in nodesConsidered:
    conceptLexicali = set(IDToLexical.get(eachConcepti))
    for eachConceptj in findAncestors(eachConcepti):
        if eachConceptj in nodesConsidered:
            conceptLexicalj = set(IDToLexical.get(eachConceptj))
            conceptLexicali = conceptLexicali.union(conceptLexicalj)
    output3.write(eachConcepti+": ")
    output3.write(" ".join(sorted(list(conceptLexicali)))+"\n")
        
output3.close()        
print "Two-step Enrichemnt Finished"       
        
#Compare lexicalfeatures_NounPhraseImproved and detect missing IS-A:    
IDToFSN = {}
file1= open("FSN.txt","rb+")
for lines in file1:
    line = lines.split("\n")[0]
    linee = line.split("\t")
    conceptID = linee[0]
    conceptFSN = linee[1]
    if IDToFSN.get(conceptID,"default") == "default":
        IDToFSN[conceptID] = conceptFSN
    else:
        if conceptFSN !=IDToFSN.get(conceptID):
            print"error"+"multiple FSN for one ID"
            print conceptID
            print conceptFSN
            print IDToFSN.get(conceptID)
            continue
file1.close()

IDToFSNFCA = {}
file1 = open("2ndEnrichedLexicalFeatures.txt","rb+")
for lines in file1:
    line = lines.split()
    conceptID = line[0].split(":")[0]
    FSNFCA = line[1:len(line)]
    IDToFSNFCA[conceptID] = FSNFCA
file1.close()


fileNodeInSub = open("nodesInHierarchyAndTheirPath.txt","w") #Efficicent Purpose
nodesInSubHierarchy = list(set(IDToFSNFCA.keys()))
print "nodes amount: "+str(len(nodesInSubHierarchy))
#For each concept, generate its whole path
nodesPath = {}
for eachNode in nodesInSubHierarchy:
    if nodesPath.get(eachNode,"default") == "default":
        allAncestors = findAncestors(eachNode)
        allDecendants = findSubHierarchy(eachNode)
        Path = allAncestors+allDecendants
        nodesPath[eachNode] = Path

for key in nodesPath.keys():
    fileNodeInSub.write(key+" "+" ".join(nodesPath.get(key))+"\n")
fileNodeInSub.close()


nodesPath2 = {}
FileNodeInCF = open("nodesInHierarchyAndTheirPath.txt","rb+")
for lines in FileNodeInCF:
    line = lines.split()
    nodesPath2[line[0]] = line
FileNodeInCF.close()

nodesInComparison = list(nodesPath2.keys())

import csv
fileMissingISA = open("MissingIS-A(Original).csv","w")
ISAWriter = csv.writer(fileMissingISA)

for i in range(0,len(nodesInComparison)):
    print i
    FSNi = IDToFSNFCA.get(nodesInComparison[i])
    bagi = set(FSNi)
    iPath = set(nodesPath2.get(nodesInComparison[i]))
    for j in range(i+1,len(nodesInComparison)):
        if nodesInComparison[j] not in iPath:
            FSNj = IDToFSNFCA.get(nodesInComparison[j])
            bagj = set(FSNj)
            if bagi.issubset(bagj):
                ISAWriter.writerow((nodesInComparison[j],nodesInComparison[i],IDToFSN.get(nodesInComparison[j]),IDToFSN.get(nodesInComparison[i])))
            else:
                if bagj.issubset(bagi):
                    ISAWriter.writerow((nodesInComparison[i],nodesInComparison[j],IDToFSN.get(nodesInComparison[i]),IDToFSN.get(nodesInComparison[j])))
fileMissingISA.close()
        
print "Pairwise Comparison finished"        
        

#Index to Word/Phrase
IndexToWP = {}
k = 0
fileFCA = open("AllFeatures.txt","rb+")
for lines in fileFCA:
    line = lines.split("\n")
    IndexToWP[str(k)] = line[0]
    k = k+1

file1 = open("1stEnrichedLexicalFeatures.txt","rb+")
output1 = open("1stEnrichedLexicalFeatures(Word).txt","w")

for lines in file1:
    line = lines.split()
    conceptID = line[0].split(":")[0]
    attrList = line[1:len(line)]
    Interpret = []
    for index in attrList:
        Interpret.append(IndexToWP.get(index))
    output1.write(conceptID+"&"+"&".join(Interpret)+"\n")
file1.close()
fileFCA.close()
output1.close() 
        
file2 = open("2ndEnrichedLexicalFeatures.txt","rb+")
output2 = open("2ndEnrichedLexicalFeatures(Word).txt","w")

for lines in file2:
    line = lines.split()
    conceptID = line[0].split(":")[0]
    attrList = line[1:len(line)]
    Interpret = []
    for index in attrList:
        Interpret.append(IndexToWP.get(index))
    output2.write(conceptID+"&"+"&".join(Interpret)+"\n")
file2.close()
output2.close() 
                

#Filter out stop word
import string
allowed = string.letters + string.digits+ " " + "." + "-" + "/" +"'s"
def check_naive(mystring):
    return all(c in allowed for c in mystring)

digits = string.digits
def check_digits(string):
    return any(d in digits for d in string)

import csv
Antonyms = {}
file2 = open("AntonymPair.txt","rb+")
file3 = open("MissingIS-A(Original).csv","rb+") 
IDToLexicalFeature2 = {}
file4 = open("SplitFSN.txt","rb+")
output1 = open("MissingIS-A(OriginalFiltered).csv","w")
ISAReader = csv.reader(file3)
ISAWriter = csv.writer(output1)

for line2 in file2:
    line2L = line2.split()
    w1 = line2L[0]
    a1 = line2L[1]
    if Antonyms.get(w1,"default") == "default":
        Antonyms[w1] = [a1]
    else:
        if a1 not in Antonyms[w1]:
            Antonyms[w1].append(a1)
    if Antonyms.get(a1,"default") == "default":
        Antonyms[a1] = [w1]
    else:
        if w1 not in Antonyms[a1]:
            Antonyms[a1].append(w1)
file2.close()

for line3 in file4:
    lineList = line3.split()
    conceptID = lineList[0]
    lexicalfeature = lineList[1:len(lineList)]
    if IDToLexicalFeature2.get(conceptID,"default") == "default":
        IDToLexicalFeature2[conceptID] = lexicalfeature
    else:
        if lexicalfeature != IDToLexicalFeature2.get(conceptID):
            print "error"
file4.close()

file5 = open("2ndEnrichedLexicalFeatures(Word).txt","rb+")     
IDToFSNFCACF = {}
for lines in file5:
    line = lines.split("\n")[0].split("&")
    conceptID = line[0]
    FSNFCACF = line[1:len(line)]
    IDToFSNFCACF[conceptID] = FSNFCACF
file5.close()


for ISArow in ISAReader:
    discardFlag = 0   #identify if there is antonym pair
    if (check_digits(ISArow[2]) == False) and (check_digits(ISArow[3]) == False):     #filter out those concept has numbers
        if (ISArow[2].startswith("'") == False) and (ISArow[3].startswith("'") == False):
            if (ISArow[2].split(" ")[len(ISArow[2].split(" "))-1] == ISArow[3].split(" ")[len(ISArow[3].split(" "))-1]): # same semantic tag
                if (len(IDToLexicalFeature2.get(ISArow[0]))>=3) and (len(IDToLexicalFeature2.get(ISArow[1]))>=3):  # filter out those concept which is too short less than 3
                    for eachWord in IDToFSNFCACF.get(ISArow[0]):
                        if Antonyms.get(eachWord,"default") !="default":
                            for eachAntonym in Antonyms.get(eachWord):
                                if eachAntonym in IDToFSNFCACF.get(ISArow[0]):
                                    discardFlag = 1
                                    break
                    for eachWord2 in IDToFSNFCACF.get(ISArow[1]):
                        if Antonyms.get(eachWord2,"default") !="default":
                            for eachAntonym2 in Antonyms.get(eachWord2):
                                if eachAntonym2 in IDToFSNFCACF.get(ISArow[1]):
                                    discardFlag = 1        
                                    break
                    if discardFlag == 0:
                        ISAWriter.writerow((ISArow[0],ISArow[1],ISArow[2],ISArow[3]))

file3.close()
output1.close()   
        
#Remove Redundancy:
#remove redundant from missing IS-A derived from DL 
#Part1  (B,C,D,E...) --> A 
missingISAInverse = {}
import csv
file5 = open("MissingIS-A(OriginalFiltered)","rb+")
ISAReader4 = csv.reader(file5)

for row4 in ISAReader4:
    if missingISAInverse.get(row4[1],"default") == "default":
        missingISAInverse[row4[1]] = [row4[0]]
    else:
        missingISAInverse[row4[1]].append(row4[0])

nodesInSubHierarchy = findSubHierarchy(subhierarchyName) 

for eachConceptNodes in nodesInSubHierarchy:
    ancestorDic[eachConceptNodes] = findAncestors(eachConceptNodes)

for keys in missingISAInverse.keys():
    potentialChild = missingISAInverse.get(keys)
    removed = potentialChild[:]
    for eachChild in potentialChild:
        seeIfRemove = set(ancestorDic.get(eachChild)) 
        for otherItems in potentialChild:
            if otherItems in seeIfRemove:
                removed.remove(eachChild)
                break
    missingISAInverse[keys] = removed
       
IDToFSN = {}
file1= open("FSN.txt","rb+")
for lines in file1:
    line = lines.split("\n")[0]
    linee = line.split("\t")
    conceptID = linee[0]
    conceptFSN = linee[1]
    if IDToFSN.get(conceptID,"default") == "default":
        IDToFSN[conceptID] = conceptFSN
    else:
        if conceptFSN !=IDToFSN.get(conceptID):
            print"error"+"multiple FSN for one ID"
            print conceptID
            print conceptFSN
            print IDToFSN.get(conceptID)
            continue
         
import csv
file1 = open("MissingIS-A(Filtered1)","w")
ISAWriter = csv.writer(file1)

for keys in missingISAInverse.keys():
    child = missingISAInverse.get(keys)
    for eachChild in child:
        ISAWriter.writerow((eachChild,keys,IDToFSN.get(eachChild),IDToFSN.get(keys)))
file1.close()

#Part2  A-->(B,C,D,E...)
missingISA = {}
import csv
file4 = open("MissingIS-A(Filtered1)","rb+")
ISAReader4 = csv.reader(file4)

for row4 in ISAReader4:
    if missingISA.get(row4[0],"default") == "default":
        missingISA[row4[0]] = [row4[1]]
    else:
        missingISA[row4[0]].append(row4[1])

for keys in missingISA.keys():
    potentialParent = missingISA.get(keys)
    removed = potentialParent[:]
    for eachParent in potentialParent:
        seeIfRemove = set(ancestorDic.get(eachParent))
        for eachAncestor in seeIfRemove:
            if eachAncestor in set(potentialParent):
                if eachAncestor in removed:
                    removed.remove(eachAncestor)
    missingISA[keys] = removed
         
import csv
file1 = open("MissingIS-A(Filtered2)","w")
ISAWriter = csv.writer(file1)

for keys in missingISA.keys():
    parent = missingISA.get(keys)
    for eachParent in parent:
        ISAWriter.writerow((keys,eachParent,IDToFSN.get(keys),IDToFSN.get(eachParent)))
file1.close()       