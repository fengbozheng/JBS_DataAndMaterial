Three folders:
	ExperimentResult: contains all detected missing IS-A relations from 17 sub-hierarchy of SNOMED CT (they are stored in csv file, use text editor to open, Excel may transfer concept IDs to scientific numbers).
	EvaluationFile: contains the original evaluation file, reviewed one by domain expert JS, and a further edited evaluation file for incorrect IS-A relations in current SNOMED CT.
	CodeForSubsumptionTest: contains a python script (JMC_SubsumptionTest.py) to generate missing IS-A relations for a specific sub-hierarchy(or hierarchy).

Subsumption Test Running Requirement:
	1. Installed Stanford CoreNLP Parser
		In this work, we use "stanford-corenlp-full-2018-10-05"
		Start the Stanford CoreNLP Parser server, use Terminal to get in to the directory of "stanford-corenlp-full-2018-10-05" and run 
		"java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos,lemma,ner,parse,depparse -status_port 9000 -port 9000 -timeout 15000 &"
	2. File contains stop words.
		e.g. StopWord.txt      format for each line: stopword+"\n"
	3. File contains antonym pairs.
		e.g. AntonymPair.txt   format for each line: word1+"\t"+its antonym+"\n"
	4. File contains concept IDs and their FSNs.
		e.g. FSN.txt           format for each line: concept ID+"\t"+its FSN+"\n"
	5. Two files contain all IS-A relations in ontology. (One is pointing from child to parent, the other is from parent to child)
		e.g. HierarchicalRelation(ChildParent).txt     format for each line: child concept ID+"\t"+parent concept ID+"\n"
			 HierarchicalRelation(ParentChild).txt     format for each line: parent concept ID+"\t"+child concept ID+"\n"

	6. Put all files and JMC_SubsumptionTest.py under the same directory.
	7. Change relative file names and assign "root concept ID for hierarchy" in JMC_SubsumptionTest.py, and run it as a whole. 
	8. The non-rundant missing IS-A relations is included in file MissingIS-A(Filtered2).csv