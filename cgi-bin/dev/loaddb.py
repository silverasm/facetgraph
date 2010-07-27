import sys
from dbsetup import *
import simplejson
import math
import re
# in-house
import keys
import util

"""
	Load the DB with the data
"""
decoder = simplejson.JSONDecoder()
wordIndex = {}

def allowed(tag):
	return tag.startswith("N") or tag.startswith("V")

def createRevertedIndex(single_words=False, bigrams=False):
	words = {}
	coOccurrenceCounts = {}
	cameraWordCounts = {} # was going to add  camera-to-word and word-to-camera
	wordCameraCounts = {} # 
	if single_words:
		for i, fileName in enumerate(os.listdir(keys.EXTRACTED_DIR)[31:32]):
			if fileName.endswith("json"):
				print fileName
				f = open(keys.EXTRACTED_DIR+os.sep+fileName)
				json = decoder.decode(f.read())
				f.close()
				for review in json["reviews"]:
					reviewCounts = {}
					for sentence in review["sentences"]:
						taggedWords = sentence["taggedSentence"].split()
						for tagged in taggedWords:
							try:
								word, tag = tagged.split("/")
								if allowed(tag):
									if word not in reviewCounts:
										reviewCounts[word] = 0
									reviewCounts[word] += 1
									if word not in coOccurrenceCounts:
										coOccurrenceCounts[word] = util.Counter()
							except:
								pass
					for word in reviewCounts.keys():
						count = reviewCounts[word]
						for otherWord in reviewCounts.keys():
							coOccurrenceCounts[word][otherWord] += count
	elif bigrams:
		for i, fileName in enumerate(os.listdir(keys.REVIEWS_TEXT_DIR)[:]):
			print "%d %s"%(i, fileName)
			f = open(keys.REVIEWS_TEXT_DIR + os.sep + fileName)
			#lines = f.readlines()
			text = re.sub("\W", " ", f.read().lower()).split()
			f.close()
			#print text # debug
			cameraName = fileName.split(".")[0].replace("-", " ").replace("_", " ")
			cameraWordCounts[cameraName] = util.Counter()
			for word in text[:]:
				w = re.sub("xx", " ", word)
				if w not in coOccurrenceCounts:
					coOccurrenceCounts[w] = util.Counter()
					wordCameraCounts[w] = util.Counter()
				cameraWordCounts[cameraName][w] += 1
				wordCameraCounts[w][cameraName] += 1
			#sys.stdout.write("\n\t")
			for word in cameraWordCounts[cameraName]:
				#sys.stdout.write(word+", ")
				count = cameraWordCounts[cameraName][word]
				for otherWord in cameraWordCounts[cameraName]:
					coOccurrenceCounts[word][otherWord] += count
	tf_idfs = {}
	camera_word_tf_idfs = {}
	ranks = {}
	totalWords = float(len(coOccurrenceCounts))
	totalCameras = float(len(cameraWordCounts.keys()))
	print totalWords
	wordCameraQueues = {}
	for i, camera in enumerate(cameraWordCounts.keys()):
		camera_word_tf_idfs[camera] = util.Counter()
		print "CAMERA-WORD %d/%d:\t%s"%(i, totalCameras, camera)
		totalWordCount = float(cameraWordCounts[camera].totalCount())
		queue = util.PriorityQueue()
		for word in cameraWordCounts[camera]:
			if word not in wordCameraQueues:
				wordCameraQueues[word] = util.PriorityQueue()
			tf = float(cameraWordCounts[camera][word])/totalWordCount
			idf = math.log(totalCameras/float(len(wordCameraCounts[word])))
			tf_idf = tf*idf
			camera_word_tf_idfs[camera][word] = tf_idf
			queue.push(word, tf_idf)
			wordCameraQueues[word].push(camera, tf_idf)
		rank = 0
		while not queue.isEmpty():
			result = queue.pop()
			score = camera_word_tf_idfs[camera][result]
			instance = WordAndCameraRI(camera, "camera", result, "word", rank, score)
			session.add(instance)
			rank += 1
		session.commit()
	
	for i, word in enumerate(wordCameraQueues.keys()):
		rank = 0
		print "WORD-CAMERA %d/%d:\t%s"%(i, totalWords, word)
		while not wordCameraQueues[word].isEmpty():
			result = wordCameraQueues[word].pop()
			score = camera_word_tf_idfs[camera][word]
			instance = WordAndCameraRI(word, "word", result, "camera", rank, score)
			session.add(instance)
			rank+=1
		session.commit()	
	camera_word_tf_idfs = None
	for i, word in enumerate(coOccurrenceCounts.keys()):
		print "WORD_WORD %d/%d:\t%s"%(i, totalWords, word)
		tf_idfs[word] = util.Counter()
		queue = util.PriorityQueue()
		totalOccurrences = float(coOccurrenceCounts[word].totalCount())
		for word2 in coOccurrenceCounts[word].keys():
			#print word2
			tf = float(coOccurrenceCounts[word][word2])/totalOccurrences
			#print tf
			idf = math.log(totalWords/float(len(coOccurrenceCounts[word2])))
			tf_idfs[word][word2] = tf*idf
			queue.push(word2, -1*tf*idf)
		rank = 0
		query = word
		while not queue.isEmpty():
			result = queue.pop()
			score = tf_idfs[query][result]
			count = coOccurrenceCounts[query][result]
			instance = WordToWordRI(query, result, rank, score, count)
			session.add(instance)
			rank += 1
		session.commit()

"""
	Maps between use words and topics
	Maps between topics and uses
"""
INPUT_DIR = "/Users/Aditi/Desktop/fxpal/CODE/ProductFeatures/mallet/"
def createCameraTopicRI():
	INPUT_FILE = INPUT_DIR+os.sep+"doc-topics-uses-bigrams500.txt"
	index = {}
	

def createTopicWordRI():
	INPUT_FILE = INPUT_DIR+os.sep+"topic-state-uses-bigrams500"	
	index = {}
	words = []
	tw = {}
	wt = {}
	f = open(INPUT_FILE)
	# count all the use-words and topics
	i = 0
	while True:
		i += 1
		try:
			line = f.readline().strip().split()
			if len(line) > 0:
				word = line[4].replace("xx", " ")
				topic = int(line[5])
				if topic not in tw:
					tw[topic] = util.Counter()
				w = int(line[3])
				if word not in index:
					index[word] = w
					words.append(word)
					wt[w] = util.Counter()
				wt[w][topic] += 1
				tw[topic][w] += 1
				print i
			else:
				break
		except ValueError:
			continue
		except IndexError:
			continue
	for topic in tw:
		print "TOPIC_WORD %d/%d"%(topic, len(tw))
		totalCount = float(tw[topic].totalCount())
		queue = util.PriorityQueue()
		for w in tw[topic]:
			queue.push(w, -1*tw[topic][w])
		rank = 0;
		while not queue.isEmpty():
			word = words[queue.pop()]
			instance = RI(topic, "topic", word, "word", rank, float(tw[topic][w])/totalCount);
			session.add(instance)
			rank += 1
		session.commit()
	for w in wt:
		print "WORD_TOPIC %d/%d"%(w, len(wt))
		totalCount = float(wt[w].totalCount())
		queue = util.PriorityQueue()
		for t in wt[w]:
			queue.push(t, -1*wt[w][t])
		rank = 0
		while not queue.isEmpty():
			topic = queue.pop()
			instance = RI(words[w], "word", topic, "topic", rank, float(wt[w][t])/totalCount)
			session.add(instance)
			rank += 1
		session.commit()
			
	
	
	
	

if __name__ =="__main__":
	#createRevertedIndex(bigrams=True) # deathly slow
	createTopicWordRI()