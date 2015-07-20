
import os
import gensim
from gensim.models import word2vec
import logging


class MySentences(object):
	def __init__(self,dirname):
		self.dirname=dirname
		self.a=[]

	def __iter__(self):
		for fname in os.listdir(self.dirname):
			for line in open(os.path.join(self.dirname, fname)):
				line=line.strip("\n")
				yield line.split(" ")


class WordsSemantics():
	def __init__(self):
		print "Class object is initialized"

	def building_vocab(self,input_dir):
		self.sentences=MySentences(input_dir)

	def training(self, size, alpha, window, min_count, workers, sg, hs, echo):
		'''size: size is the dimensions of the feature vectors for any word.
		alpha: alpha is the learning rate.
	   	window: window is the maximum distance between the current and predictive words within a sentence
	   	min_count: ignore those words on a corpus whose count is less than min_count
	   	workers: use as many workers to train the model faster(faster training with multicore machines)
	   	sg: By default skip grams is used(=1) else Cbow (Continuous bag of words) algorithm is used.
	   	hs: By default hierarchical sampling will be used for model training 
	   	iter: Number of echos used for training the model.'''

	   	model = word2vec.Word2Vec(self.sentences, size=size, alpha=alpha, window=window, min_count=min_count, workers=workers, sg=sg, hs=hs, iter=echo)
	   	##logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
		return model

	def saving_model(self,model,saving_dir):
		'''model: model is a trained model'''

		model.save(saving_dir+r'/train.model') ##This is for saving the entire model including weights and vectors
		model.save_word2vec_format(saving_dir+r'/train.model.bin', binary=True) ## for saving words with corresponding vectors

	def loading_model(self,loading_dir):

		return word2vec.Word2Vec.load_word2vec_format(loading_dir+r'/train.model.bin', binary=True) ## for loading the trained words with the vectors

	def most_similar(self,model,query_word,topn):

		return model.most_similar([query_word],topn=topn)

	def get_vector(self,model,query_word):

		return model[query_word]  ##will return the vector of the query word

	def similarity_between_sets(self,model,list_a,list_b):

		return model.n_similarity(list_a,list_b)   ## giving the similarity between two set of words

	def similarity_between_words(self,word_a,word_b):

		return model.similarity(word_a,word_b)   ## giving the similarity between two words





