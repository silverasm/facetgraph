'''
Created on Jun 4, 2010

@author: Aditi

Configuration - mostly laying out where various files and directories
are

'''

from os import sep

#BASE_DIR = "/home/shrikumar"
#CODE_DIR = BASE_DIR +sep+"code/datamining/informationextraction"
#SHARED_DIR = "/net/palnas2/exports/vol1/DiG/extracted"
#DATA_DIR = BASE_DIR+sep+"data"


BASE_DIR = "/Users/Aditi/Desktop/fxpal/CODE/ProductFeatures"
CODE_DIR = BASE_DIR+sep+"com/fxpal/datamining/informationextraction"
DATA_DIR = BASE_DIR+sep+"data"
SHARED_DIR = DATA_DIR


NP_CHUNKER_CLASSIFIER = DATA_DIR +sep+"NPchunkerclassifier.pickle"
alphabet = "abcdefghijklmnopqrstuvwxyz"
referenceAdjectives = ["excellent", "fantastic", 
                       "outstanding", "wonderful", 
                       "amazing", "great", 
                       "poor", "okay", 
                       "adequate", "ordinary", 
                       "awful", "horrible", 
                       "terrible", "lousy", "inferior"]
#referenceAdjectives = ["excellent","fantastic", "terrible", "awful" ]
refAdjSets=[("excellent", "terrible"), ("fantastic", "awful"), ("wonderful", "horrible"), ("outstanding", "inferior"), ("amazing", "adequate", "lousy")]
#GOOGLE_API_KEY = ""
#GOOGLE_API_URL = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="
YAHOO_API_URL = "http://boss.yahooapis.com/ysearch/web/v1/"
YAHOO_API_KEY = "6iyIHN3V34GOaezyUe7vklkWgr8IxzuPoSyN3D6byWVYHmdwMaSS6QsiiUP7G3r1fy2zp4R9"

SENTENCES_DIR = DATA_DIR+sep+"sentences"
PARSED_SENTENCES_DIR = DATA_DIR+sep+"parses"
EXTRACTIONS_DIR = DATA_DIR+sep+"extractions"
REVIEWS_DIR = DATA_DIR+sep+"reviewsentences"
ALL_REVIEWS = REVIEWS_DIR+sep+"allreviews.txt"
ALL_REVIEWS_PARSED= "allreviews.txt.parsed"

PARSER_DIR = CODE_DIR+sep+"parser"
PARSER = PARSER_DIR+sep+"lexparser.csh"

TREGEX_DIR = CODE_DIR+sep+"tregex"
TREGEX = TREGEX_DIR+sep+"tregex.sh"

TUNE_DIR = DATA_DIR+sep+"tune"
MODELS_DIR = DATA_DIR+sep+"models" #where the SVM models are stored
TMP_DIR = DATA_DIR+sep+"tmp" #where temporary files live

HIT_COUNTS = MODELS_DIR+sep+"hitcounts.txt"
loaded = False
accesses = 0

#distributed computing
CATS = ["cat01:8001", "cat02:8002", "cat03:8003", "cat04:8004"]
MULTI_CATS = CATS*4
MAIL = "aditi.shrikumar@gmail.com"
SERVER_CODE_DIR = "/home/shrikumar/code/datamining/informationextraction"
QUERY = SERVER_CODE_DIR+sep+"query.py" # queries the web for sentences
PARSE = SERVER_CODE_DIR+sep+"parse.py" # parses all the sentences 
EXTRACT = SERVER_CODE_DIR+sep+"extract.py"
FILTER_FACTS = SERVER_CODE_DIR+sep+"filterfacts.py"

# where shared files live
EXTRACTED_DIR = SHARED_DIR+sep+"hierarchy" #prev: featurevectors, prev: uses_NC_opinions
CLEANED_DIR = SHARED_DIR+sep+"all_identified" # prev: hierarchy, featurevectors
REVIEWS_TEXT_DIR = SHARED_DIR+sep+"mallet-input/reviewsentences_bigrams"
# camera clustering by feature etc.
CLUSTERING_DIR = SHARED_DIR+sep+"clusters"
LEXICON = CLUSTERING_DIR+sep+"lexicon.tff"
FEATURE_COUNTS = CLUSTERING_DIR+sep+"featureCounts.txt"
USE_COUNTS = CLUSTERING_DIR+sep+"useCounts.txt"
USE_FEATURE_COUNTS = CLUSTERING_DIR+sep+"useFeatureCounts.csv"
FEATURE_USE_COUNTS = CLUSTERING_DIR+sep+"featureUseCounts.csv"
# clusters of features
TERMS_DIR = SHARED_DIR+sep+"terms"
TERMS_FILE = TERMS_DIR +sep+"NP_adjNsubj_LC_ALL.similarity"
CLUSTERS_FILE = TERMS_DIR+sep+"clusters.20.txt"
FEATURE_CLUSTERS = TERMS_DIR+sep+"reliableCamFeatGroupsCnts.txt" # previous: camFeatGroups.txt
FEATURE_TREE = CLUSTERING_DIR+sep+"featureHierarchy.txt"
# reverted indexing
REVERTED_INDEX_DIR = SHARED_DIR +sep+"revertedindex"

# opinion estimate shrinkage
N_ITERATIONS = 10
PRIOR_POSITIVE = 1.0 # the proportion of positive to negative
PRIOR_NEGATIVE = 1.0 # used as input for a beta distribution, so must be > 1