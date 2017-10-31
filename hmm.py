from __future__ import division
import numpy as np
from math import log
import pickle
from pprint import pprint
file = open("Training set.txt" ,"r")
data = file.readlines()

# 3 tables to be maintained
#tag*tag = tag1 given tag2
#maintain count of tag
#For each word  corresponding how may times tag appear word*tag
def createDict():
	tags = {}
	for line in data:
		if line not in ["\n" ,"\r\n"]:
			words = line.split("\t")
			#print len(words) ,
			tag = words[1]
			tag = tag.strip("\n")
			
			if  tag not in tags.keys():
				tags[tag ] = [] 
			if words[0] not in tags[tag]:
				tags[tag].append(words[0])
	return tags
	
	
def viterbi(obs ):
	T = len( obs )
	N = len(wordTag)
	L = len(transition) - 2
	viterbi = {}
	for i in transition.keys():
		if i not in ["s"]:
			viterbi[i] = {}
			for j in range ( T ):
				viterbi[i][j] = []
			
	for s in viterbi.keys():
		if s not in ["s" , "."]:
			if obs[0] in wordTag.keys():
				viterbi[s][0].append( log (transition[s]["s"])+log (wordTag[obs[0]][s]) )
				viterbi[s][0].append("s")
			else:
				viterbi[s][0].append( log (transition[s]["s"])+log(1/N)) #probability
				viterbi[s][0].append("s")
				
	for t in range(1, T):
		for s in viterbi.keys():
			if s not in ["." ,"s"]:
				temp = []
				word = obs[t]
				
				for i in viterbi.keys() :
					if i not in ["." , "s"] :	
						if word in wordTag.keys():
							b = wordTag[word][s] #emission prob
						else:
							if i in [ "NN" ,"VBP", "JJ", "RB" ]:
								b = 1/5
							else:
								b = (1/5)*(1/(L- 4))
								#print b #To be done for unknown words
						a = viterbi[i][t-1][0]+ log (transition[s][i]) + log (b)
						temp.append(a)
				m = max ( temp )
				ctr = 0
				for i in viterbi.keys() :
					if i not in ["." , "s"] :					
						if temp[ctr] == m:
							#backpointer[s][t].append(i)
							viterbi[s][t].append(m)
							viterbi[s][t].append(i)
							break
						ctr += 1
				
				
	temp = []
	for i in viterbi.keys() :
		if i  not in ["." , "s"] :					
			a = viterbi[i][T-1][0]+ log(transition["."][i])
			temp.append(a)
	m = max(temp)
	#backpointer[s][t] = []
	#m = max(temp)
	ctr = 0
	for i in viterbi.keys() :
		if i not in ["." , "s"] :					
			if temp[ctr] == m:
				#backpointer[s][t].append(i)
				viterbi["."][T-1].append(m)
				viterbi["."][T-1].append(i)
			ctr += 1
	
	return  viterbi

def doTest ():
	file = open("test_set.txt" ,"r")
	#output = open ()
	data = file.readlines()
	sentence =[]
	with open("Output.txt" , "w") as output:
		for line in data:
			#print line
			if line not in ["\n" ,"\r\n"]:
				#print "here"
				if "." in line:
					ans = do_viterbi (sentence)
					#print ans , sentence
					for i,j in zip(  sentence, ans):
						#print "hola"
						if i == "and\n":
							j = "CC"
						a = i.strip("\n")+"\t"+j
						#print a
						output.write(a+ '\n')
					output.write(".\t.\n\n")
					sentence =[]
				else:
					sentence.append(line)
	output.close()
#Created tag table
def createTagTable ():
	prev = "s"
	for line in data:
		if line not in ["\n" ,"\r\n"]:
			words = line.split("\t")
			#print len(words) ,
			tag = words[1]
			tag = tag.strip("\n")
			# print tag
			# print prev
			transition[tag][prev] += 1
			if tag == ".":
				prev = "s"
			else:
				prev = tag

def getCountOfTags ():
	countTag = {}
	for i in tags.keys():
		countTag[i] = 0
	for line in data:
		if line not in ["\n" ,"\r\n"]:
			words = line.split("\t")
			#print len(words) ,
			tag = words[1]
			tag = tag.strip("\n")
			countTag[tag] += 1
	return countTag


def calculateTransition ():
	for i in transition.keys():
		for j in transition.keys():
			transition[i][j] = transition[i][j]/( countTag[j]+ len(transition.keys() ) ) 


def calculateEmission ():
	N = len(countTag) -2 
	for i in wordTag.keys():
		for j in wordTag[i]:
			wordTag [i][j] += 1 
			wordTag[i][j] /= (countTag[j] + N)


if __name__ == "__main__":
	file = open("Training set.txt" ,"r")
	data = file.readlines()
	mydict = createDict()
	output = open('Dictionary.pkl', 'wb')
	pickle.dump(mydict, output)
	output.close()

	# read python dict back from the file
	pkl_file = open('Dictionary.pkl', 'rb')
	tags = pickle.load(pkl_file)
	pkl_file.close()

	#Initalising Transition table
	transition = {}
	for k in tags.keys():
		transition[k] = {}
	transition["s"] = {}
	for i in transition.keys():
		for j in transition.keys():
			transition[i][j] = 0
	
	createTagTable()
	doSmoothing()
	output = open('TagTable.pkl', 'wb')
	pickle.dump(transition, output)
	output.close()

	#read python dict back from the file
	pkl_file = open('TagTable.pkl', 'rb')
	transition = pickle.load(pkl_file)
	pkl_file.close()
	wordTag = createWordTag()
	output = open('WordTagTable.pkl', 'wb')
	pickle.dump(wordTag, output)
	output.close()

	#read python dict back from the file
	pkl_file = open('WordTagTable.pkl', 'rb')
	wordTag = pickle.load(pkl_file)
	pkl_file.close()
	#print len(wordTag)
	countTag = getCountOfTags()
	#print countTag	
	countTag ["s" ] = countTag["."]
	calculateTransition()
	calculateEmission()
	doTest()
